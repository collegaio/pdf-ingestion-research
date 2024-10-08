import tempfile
import glob
import os

import polars as pl
import s3fs


def download_parquet_files(input_folder: str, output_folder: str):
    fs = s3fs.S3FileSystem()

    with tempfile.TemporaryDirectory() as tempdir:
        fs.get(input_folder, tempdir, recursive=True)

        # TODO: split up all the code so it can run in Lambda
        df_files = glob.glob("*.parquet", root_dir=tempdir, recursive=True)
        main_df = pl.DataFrame()

        for file in df_files:
            df = pl.read_parquet(os.path.join(tempdir, file)).with_columns(
                dataset_id=pl.lit(os.path.splitext(file)[0])
            )
            main_df = pl.concat([main_df, df], how="diagonal_relaxed")

        output_filename = f"{os.path.basename(input_folder.rstrip('/'))}.csv"

        main_outfile = os.path.join(tempdir, output_filename)
        remote_outfile = os.path.join(output_folder, output_filename)

        main_df.write_csv(main_outfile)

        fs.put(main_outfile, remote_outfile)


if __name__ == "__main__":
    download_parquet_files(
        "s3://collega-dataframes-533267152364/cds_files/",
        "s3://collega-dataframes-533267152364/combined/",
    )
