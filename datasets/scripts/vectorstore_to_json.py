import json
import os
import dotenv
import asyncio

from llama_index.core import VectorStoreIndex
from llama_index.core.llms import LLM
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from dataset_tools.cds.models import (
    AcceptedApplicantInfo,
    AdmissionsFactorWeights,
    AdmissionsRequirementsInfo,
    CDSDataset,
    ClassRankInfo,
    GPAInfo,
    InstitutionCDSInfo,
    ResidencyInfo,
    StandardizedTestScoreInfo,
    WaitListInfo,
)

from dataset_tools.parsing.structured import query_structured_output

dotenv.load_dotenv("../.env")

llama_cloud_api_key = os.environ["LLAMA_CLOUD_API_KEY"]
openai_api_key = os.environ["OPENAI_API_KEY"]
pinecone_api_key = os.environ["PINECONE_API_KEY"]

pinecone_index_name = "cds-index-test"


async def build_cds_info_json(dataset_id: str, index: VectorStoreIndex, llm: LLM):
    accepted_applicant_info: AcceptedApplicantInfo = await query_structured_output(
        query="What is the breakdown of male and female first year applicant?",
        dataset_id=dataset_id,
        index=index,
        llm=llm,
        output_cls=AcceptedApplicantInfo,
    )

    print(accepted_applicant_info)

    residency_info: ResidencyInfo = await query_structured_output(
        query="What is the residency breakdown for first year applicants, admits, and enrolled students?",
        dataset_id=dataset_id,
        index=index,
        llm=llm,
        output_cls=ResidencyInfo,
    )

    print(residency_info)

    waitlist_info: WaitListInfo = await query_structured_output(
        query="Does this school offer a waitlist and how many students were placed on it and admitted from it?",
        dataset_id=dataset_id,
        index=index,
        llm=llm,
        output_cls=WaitListInfo,
    )

    print(waitlist_info)

    admissions_requirements_info: AdmissionsRequirementsInfo = (
        await query_structured_output(
            query="What high school course credits required or recommended for admission?",
            dataset_id=dataset_id,
            index=index,
            llm=llm,
            output_cls=AdmissionsRequirementsInfo,
        )
    )

    print(admissions_requirements_info)

    admissions_factor_weights: AdmissionsFactorWeights = await query_structured_output(
        query="What is the breakdown of relative importance of academic and nonacademic factors for admitted students?",
        dataset_id=dataset_id,
        index=index,
        llm=llm,
        output_cls=AdmissionsFactorWeights,
    )

    print(admissions_factor_weights)

    standardized_test_score_info: StandardizedTestScoreInfo = (
        await query_structured_output(
            query="What is the breakdown of SAT or ACT test scores for admitted students?",
            dataset_id=dataset_id,
            index=index,
            llm=llm,
            output_cls=StandardizedTestScoreInfo,
        )
    )

    print(standardized_test_score_info)
    # class_rank_info: ClassRankInfo = Field(
    #     description="Information about class rank of students at this institution"
    # )
    class_rank_info: ClassRankInfo = await query_structured_output(
        query="What is the breakdown of class rank placement for admitted students?",
        dataset_id=dataset_id,
        index=index,
        llm=llm,
        output_cls=ClassRankInfo,
    )

    print(class_rank_info)

    gpa_info: GPAInfo = await query_structured_output(
        query="What is the breakdown of GPA scores of admitted students?",
        dataset_id=dataset_id,
        index=index,
        llm=llm,
        output_cls=GPAInfo,
    )

    print(gpa_info)

    # fees: ApplicationFees = await query_structured_output(
    #     query="What is the application fee for applying to this school?",
    #     dataset_id=dataset_id,
    #     index=index,
    #     llm=llm,
    #     output_cls=ApplicationFees,
    # )

    # print(fees)

    cds_info = InstitutionCDSInfo(
        accepted_applicant_info=accepted_applicant_info,
        residency_info=residency_info,
        waitlist_info=waitlist_info,
        admissions_requirements_info=admissions_requirements_info,
        admissions_factor_weights=admissions_factor_weights,
        standardized_test_score_info=standardized_test_score_info,
        class_rank_info=class_rank_info,
        gpa_info=gpa_info,
        # fees=fees,
    )

    print(cds_info)

    with open(f"../cds/json/{dataset_id}.json", "w") as fp:
        fp.write(cds_info.model_dump_json())


async def main():
    llm = OpenAI(api_key=openai_api_key)
    pc = Pinecone(api_key=pinecone_api_key)

    index = VectorStoreIndex.from_vector_store(
        vector_store=PineconeVectorStore(pc.Index(pinecone_index_name))
    )

    # Run on all datasets
    # TODO: skip missing indexes + warning
    with open("../../datasets.json", "r") as fp:
        datasets = [CDSDataset(**doc) for doc in json.load(fp)["cds-files"]][11:12]

    asyncio.gather(
        (build_cds_info_json(dataset.id, index, llm) for dataset in datasets)
    )


if __name__ == "__main__":
    asyncio.run(main())
