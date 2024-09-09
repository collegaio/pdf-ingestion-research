from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from dataset_tools.parsing.structured import Column

# CDS_COLUMNS = [
#     Column(name="academic_year_calendar", datatype="string"),
# ]

CDS_COLUMNS = [
    Column(name="institution_requires_high_school_completion", datatype="boolean"),
    Column(
        name="are_first_time_first_year_students_accepted_for_terms_other_than_the_fall",
        datatype="boolean",
    ),
    Column(
        name="institution_requires_or_recommends_college_preparatory_program",
        datatype="boolean",
    ),
    Column(
        name="institution_allow_students_to_postpone_enrollment_after_admission",
        datatype="boolean",
    ),
    Column(name="maximum_period_of_postponement", datatype="string"),
    Column(name="average_high_school_gpa", datatype="number"),
    Column(
        name="percent_of_total_first_time_first_year_students_who_submitted_high_school_gpa",
        datatype="number",
    ),
    Column(
        name="do_tuition_and_fees_vary_by_undergraduate_instructional_program",
        datatype="string",
    ),
    Column(
        name="percent_of_full_time_undergraduates_pay_more_than_the_tuition_and_fees_reported_in_g1",
        datatype="string",
    ),
    Column(name="institution_has_application_closing_date", datatype="boolean"),
    Column(name="application_closing_date_fall", datatype="string"),
    Column(name="application_priority_date", datatype="string"),
    Column(name="has_waiting_list_policy", datatype="boolean"),
    Column(
        name="number_of_qualified_applicants_offered_a_place_on_waiting_list",
        datatype="integer",
    ),
    Column(name="number_accepting_a_place_on_the_waiting_list", datatype="integer"),
    Column(name="number_of_wait_listed_students_admitted", datatype="integer"),
    Column(name="is_waiting_list_ranked", datatype="boolean"),
    Column(name="net_price_calculator_url", datatype="string"),
    Column(name="tuition_and_fee_data_status", datatype="string"),
    Column(name="academic_costs_available", datatype="string"),
    Column(name="approximate_date_costs_available", datatype="string"),
    Column(
        name="are_notifications_to_applicants_of_admission_decision_sent_on_a_rolling_basis",
        datatype="boolean",
    ),
    Column(name="what_date_do_rolling_notifications_begin", datatype="string"),
    Column(
        name="notifications_of_admission_decision_sent_by_date",
        datatype="string",
    ),
    Column(name="deadline_for_housing_deposits", datatype="string"),
    Column(name="amount_of_housing_deposit_dollars", datatype="number"),
    Column(
        name="housing_deposits_refundable_if_student_does_not_enroll",
        datatype="boolean",
    ),
    Column(
        name="in_district_students_per_credit_hour_charge_tuition_only_dollars",
        datatype="number",
    ),
    Column(
        name="in_state_out_of_district_students_per_credit_hour_charge_tuition_only_dollars",
        datatype="number",
    ),
    Column(
        name="out_of_state_students_per_credit_hour_charge_tuition_only_dollars",
        datatype="number",
    ),
    Column(
        name="international_non_resident_students_per_credit_hour_charge_tuition_only_dollars",
        datatype="number",
    ),
    Column(name="has_application_fee", datatype="boolean"),
    Column(name="amount_of_application_fee_dollars", datatype="number"),
    Column(
        name="can_the_fee_be_waived_for_applicants_with_financial_need",
        datatype="boolean",
    ),
    Column(name="has_fee_if_applying_online", datatype="boolean"),
    Column(
        name="can_the_fee_be_waived_for_students_with_financial_need",
        datatype="boolean",
    ),
    Column(
        name="percent_in_top_tenth_of_high_school_graduating_class_percent",
        datatype="number",
    ),
    Column(
        name="percent_in_top_quarter_of_high_school_graduating_class_percent",
        datatype="number",
    ),
    Column(
        name="percent_in_top_half_of_high_school_graduating_class_percent",
        datatype="number",
    ),
    Column(
        name="percent_in_bottom_half_of_high_school_graduating_class_percent",
        datatype="number",
    ),
    Column(
        name="percent_in_bottom_quarter_of_high_school_graduating_class_percent",
        datatype="number",
    ),
    Column(
        name="percent_of_total_first_time_first_year_students_who_submitted_high_school_class_rank_percent",
        datatype="number",
    ),
    Column(name="institution_offers_early_decision_plan", datatype="boolean"),
    Column(name="first_or_only_early_decision_plan_closing_date", datatype="string"),
    Column(
        name="first_or_only_early_decision_plan_notification_date", datatype="string"
    ),
    Column(name="other_early_decision_plan_closing_date", datatype="string"),
    Column(name="other_early_decision_plan_notification_date", datatype="string"),
    Column(
        name="number_of_early_decision_applications_received_by_your_institution",
        datatype="integer",
    ),
    Column(
        name="number_of_applicants_admitted_under_early_decision_plan",
        datatype="integer",
    ),
    Column(
        name="significant_details_about_early_decision_plan",
        datatype="string",
    ),
    Column(
        name="has_a_nonbinding_early_action_plan",
        datatype="boolean",
    ),
    Column(name="early_action_closing_date", datatype="string"),
    Column(name="early_action_notification_date", datatype="string"),
    Column(
        name="is_your_early_action_plan_a_restrictive_plan_under_which_you_limit_students_from_applying_to_other_early_plans",
        datatype="boolean",
    ),
    Column(
        name="number_of_early_action_applications_received_by_your_institution",
        datatype="integer",
    ),
    Column(
        name="number_of_applicants_admitted_under_early_action_plan", datatype="integer"
    ),
    Column(
        name="number_of_applicants_enrolled_under_early_action_plan", datatype="integer"
    ),
    Column(
        name="estimated_expenses_books_and_supplies_residents_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_books_and_supplies_commuters_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_books_and_supplies_commuters_not_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_housing_only_commuters_not_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_food_only_commuters_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_food_only_commuters_not_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_transportation_residents_dollars", datatype="number"
    ),
    Column(
        name="estimated_expenses_transportation_commuters_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="estimated_expenses_transportation_commuters_not_living_at_home_dollars",
        datatype="number",
    ),
    Column(name="estimated_other_expenses_residents_dollars", datatype="number"),
    Column(
        name="estimated_other_expenses_commuters_living_at_home_dollars",
        datatype="number",
    ),
    Column(
        name="other_expenses_commuters_not_living_at_home_dollars", datatype="number"
    ),
    Column(name="high_school_units_academic_units_required", datatype="integer"),
    Column(name="high_school_units_required_english", datatype="integer"),
    Column(name="high_school_units_required_mathematics", datatype="integer"),
    Column(name="high_school_units_required_science", datatype="integer"),
    Column(name="high_school_units_required_science_lab", datatype="integer"),
    Column(name="high_school_units_required_foreign_language", datatype="integer"),
    Column(name="high_school_units_required_social_studies", datatype="integer"),
    Column(name="high_school_units_required_history", datatype="integer"),
    Column(name="high_school_units_required_computer_science", datatype="integer"),
    Column(
        name="high_school_units_required_visual_performing_arts", datatype="integer"
    ),
    Column(name="high_school_units_required_academic_electives", datatype="integer"),
    Column(name="percent_who_had_gpa_of_4", datatype="number"),
    Column(name="percent_who_had_gpa_between_3_75_and_3_99", datatype="number"),
    Column(name="percent_who_had_gpa_between_3_50_and_3_74", datatype="number"),
    Column(name="percent_who_had_gpa_between_3_25_and_3_49", datatype="number"),
    Column(name="percent_who_had_gpa_between_3_00_and_3_24", datatype="number"),
    Column(name="percent_who_had_gpa_between_2_50_and_2_99", datatype="number"),
    Column(name="percent_who_had_gpa_between_2_0_and_2_49", datatype="number"),
    Column(name="percent_who_had_gpa_between_1_0_and_1_99", datatype="number"),
    Column(name="percent_who_had_gpa_below_1", datatype="number"),
    Column(name="percent_of_students_who_did_not_submit_scores", datatype="number"),
    Column(name="percent_of_all_enrolled_students", datatype="number"),
    Column(name="importance_rigor_of_secondary_school_record", datatype="string"),
    Column(name="importance_class_rank", datatype="string"),
    Column(name="importance_academic_grade_point_average_gpa", datatype="string"),
    Column(name="importance_recommendations", datatype="string"),
    Column(name="importance_standardized_test_scores", datatype="string"),
    Column(name="importance_application_essay", datatype="string"),
    Column(name="importance_interview", datatype="string"),
    Column(name="importance_extracurricular_activities", datatype="string"),
    Column(name="importance_talent_ability", datatype="string"),
    Column(name="importance_character_personal_qualities", datatype="string"),
    Column(name="importance_first_generation", datatype="string"),
    Column(name="importance_alumni_ae_relation", datatype="string"),
    Column(name="importance_geographical_residence", datatype="string"),
    Column(name="importance_state_residency", datatype="string"),
    Column(name="importance_religious_affiliation_commitment", datatype="string"),
    Column(name="importance_volunteer_work", datatype="string"),
    Column(name="importance_work_experience", datatype="string"),
    Column(name="importance_level_of_applicant_interest", datatype="string"),
    Column(name="submitting_sat_scores_percent", datatype="number"),
    Column(name="submitting_sat_scores_number", datatype="integer"),
    Column(name="submitting_act_scores_percent", datatype="number"),
    Column(name="submitting_act_scores_number", datatype="integer"),
    Column(name="sat_composite_25th_percentile_score", datatype="integer"),
    Column(name="sat_composite_75th_percentile_score", datatype="integer"),
    Column(
        name="sat_evidence_based_reading_and_writing_25th_percentile_score",
        datatype="integer",
    ),
    Column(
        name="sat_evidence_based_reading_and_writing_75th_percentile_score",
        datatype="integer",
    ),
    Column(name="sat_math_25th_percentile_score", datatype="integer"),
    Column(name="sat_math_75th_percentile_score", datatype="integer"),
    Column(name="act_composite_25th_percentile_score", datatype="integer"),
    Column(name="act_composite_75th_percentile_score", datatype="integer"),
    Column(name="act_math_25th_percentile_score", datatype="integer"),
    Column(name="act_math_75th_percentile_score", datatype="integer"),
    Column(name="act_english_25th_percentile_score", datatype="integer"),
    Column(name="act_english_75th_percentile_score", datatype="integer"),
    Column(name="act_reading_25th_percentile_score", datatype="integer"),
    Column(name="act_reading_75th_percentile_score", datatype="integer"),
    Column(name="act_science_25th_percentile_score", datatype="integer"),
    Column(name="act_science_75th_percentile_score", datatype="integer"),
    Column(
        name="total_first_time_first_year_men_applied_fall_2023", datatype="integer"
    ),
    Column(
        name="total_first_time_first_year_women_applied_fall_2023", datatype="integer"
    ),
    Column(
        name="total_first_time_first_year_men_admitted_fall_2023", datatype="integer"
    ),
    Column(
        name="total_first_time_first_year_women_admitted_fall_2023", datatype="integer"
    ),
    Column(
        name="total_first_time_first_year_men_enrolled_fall_2023", datatype="integer"
    ),
    Column(
        name="total_first_time_first_year_women_enrolled_fall_2023", datatype="integer"
    ),
    Column(
        name="full_time_first_time_first_year_men_enrolled_fall_2023",
        datatype="integer",
    ),
    Column(
        name="full_time_first_time_first_year_women_enrolled_fall_2023",
        datatype="integer",
    ),
    Column(
        name="part_time_first_time_first_year_men_enrolled_fall_2023",
        datatype="integer",
    ),
    Column(
        name="part_time_first_time_first_year_women_enrolled_fall_2023",
        datatype="integer",
    ),
    Column(name="total_first_time_first_year_in_state_applied", datatype="integer"),
    Column(name="total_first_time_first_year_out_of_state_applied", datatype="number"),
    Column(name="total_first_time_first_year_international_applied", datatype="number"),
    Column(name="total_first_time_first_year_total_applied", datatype="number"),
    Column(name="total_first_time_first_year_in_state_admitted", datatype="number"),
    Column(name="total_first_time_first_year_out_of_state_admitted", datatype="number"),
    Column(
        name="total_first_time_first_year_international_admitted", datatype="number"
    ),
    Column(name="total_first_time_first_year_total_admitted", datatype="number"),
    Column(name="total_first_time_first_year_in_state_enrolled", datatype="number"),
    Column(name="total_first_time_first_year_out_of_state_enrolled", datatype="number"),
    Column(
        name="total_first_time_first_year_international_enrolled", datatype="number"
    ),
    Column(name="total_first_time_first_year_total_enrolled", datatype="number"),
    Column(name="name_of_college_or_university", datatype="string"),
    # Column(name="street_address", datatype="string"),
    # Column(name="address_city", datatype="string"),
    # Column(name="address_state", datatype="string"),
    # Column(name="address_zip", datatype="integer"),
    # Column(name="address_country", datatype="string"),
    # Column(name="main_institution_phone_number", datatype="string"),
    # Column(name="main_institution_website", datatype="string"),
    # Column(name="main_institution_email", datatype="string"),
    # Column(name="admissions_office_street_address", datatype="string"),
    # Column(name="admissions_office_city", datatype="string"),
    # Column(name="admissions_office_state", datatype="string"),
    # Column(name="admissions_office_zip", datatype="integer"),
    # Column(name="admissions_office_country", datatype="string"),
    # Column(name="admissions_office_phone_number", datatype="string"),
    # Column(name="admissions_office_toll_free_number", datatype="string"),
    # Column(name="admissions_office_website", datatype="string"),
    # Column(name="admissions_office_email_address", datatype="string"),
    # Column(name="separate_url_for_online_application", datatype="string"),
    Column(name="source_of_institutional_control", datatype="string"),
    Column(name="classify_your_undergraduate_institution", datatype="string"),
    Column(name="academic_year_calendar", datatype="string"),
    Column(
        name="public_institution_tuition_in_district_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_in_district_undergraduate_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_in_state_out_of_district_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_in_state_out_of_district_undergraduate_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_out_of_state_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_out_of_state_undergraduate_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_international_non_resident_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="public_institution_tuition_international_non_resident_undergraduate_dollars",
        datatype="number",
    ),
    Column(name="all_institutions_required_fees_first_year_dollars", datatype="number"),
    Column(
        name="all_institutions_required_fees_undergraduate_dollars", datatype="number"
    ),
    Column(
        name="all_institutions_food_and_housing_on_campus_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="all_institutions_food_and_housing_on_campus_undergraduate_dollars",
        datatype="number",
    ),
    Column(
        name="all_institutions_housing_only_on_campus_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="all_institutions_housing_only_on_campus_undergraduate_dollars",
        datatype="number",
    ),
    Column(
        name="all_institutions_food_only_on_campus_meal_plan_first_year_dollars",
        datatype="number",
    ),
    Column(
        name="all_institutions_food_only_on_campus_meal_plan_undergraduate_dollars",
        datatype="number",
    ),
    Column(name="minimum_number_of_credits", datatype="number"),
    Column(name="do_tuition_and_fees_vary_by_year_of_study", datatype="boolean"),
    Column(name="initial_2016_cohort_pell_grant_recipients", datatype="number"),
    Column(
        name="initial_2016_cohort_stafford_loan_recipients_no_pell_grant",
        datatype="number",
    ),
    Column(
        name="initial_2016_cohort_no_pell_grant_or_stafford_loan", datatype="number"
    ),
    Column(name="initial_2016_cohort_total", datatype="number"),
    Column(
        name="non_persisting_non_graduating_2016_cohort_pell_grant_recipients",
        datatype="number",
    ),
    Column(
        name="non_persisting_non_graduating_2016_cohort_no_pell_grant_or_stafford_loan",
        datatype="number",
    ),
    Column(name="non_persisting_non_graduating_2016_cohort_total", datatype="number"),
    Column(name="final_2016_cohort_pell_grant_recipients", datatype="number"),
    Column(
        name="final_2016_cohort_stafford_loan_recipients_no_pell_grant",
        datatype="number",
    ),
    Column(name="final_2016_cohort_no_pell_grant_or_stafford_loan", datatype="number"),
    Column(name="final_2016_cohort_total", datatype="number"),
    Column(name="completed_within_4_years_pell_grant_recipients", datatype="number"),
    Column(
        name="completed_within_4_years_stafford_loan_recipients_no_pell_grant",
        datatype="number",
    ),
    Column(
        name="completed_within_4_years_no_pell_grant_or_stafford_loan",
        datatype="number",
    ),
    Column(name="completed_within_4_years_total", datatype="number"),
    Column(name="completed_within_5_years_pell_grant_recipients", datatype="number"),
    Column(
        name="completed_within_5_years_stafford_loan_recipients_no_pell_grant",
        datatype="number",
    ),
    Column(
        name="completed_within_5_years_no_pell_grant_or_stafford_loan",
        datatype="number",
    ),
    Column(name="completed_within_5_years_total", datatype="number"),
    Column(name="completed_within_6_years_pell_grant_recipients", datatype="number"),
    Column(
        name="completed_within_6_years_stafford_loan_recipients_no_pell_grant",
        datatype="number",
    ),
    Column(
        name="completed_within_6_years_no_pell_grant_or_stafford_loan",
        datatype="number",
    ),
    Column(name="completed_within_6_years_total", datatype="number"),
    Column(name="graduating_within_6_years_total", datatype="number"),
    Column(name="graduating_within_6_years_pell_grant_recipients", datatype="number"),
    Column(
        name="graduating_within_6_years_stafford_loan_recipients_no_pell_grant",
        datatype="number",
    ),
    Column(
        name="graduating_within_6_years_no_pell_grant_or_stafford_loan",
        datatype="number",
    ),
    Column(
        name="six_year_graduation_rate_pell_grant_recipients_percent", datatype="number"
    ),
    Column(
        name="six_year_graduation_rate_stafford_loan_recipients_no_pell_grant_percent",
        datatype="number",
    ),
    Column(
        name="six_year_graduation_rate_no_pell_grant_or_stafford_loan_percent",
        datatype="number",
    ),
    Column(name="six_year_graduation_rate_total_percent", datatype="number"),
    # Column(name="agriculture_diploma_certificates_percent", datatype="number"),
    # Column(name="agriculture_associate_percent", datatype="number"),
    # Column(name="agriculture_bachelors_percent", datatype="number"),
    # Column(
    #     name="natural_resources_and_conservation_diploma_certificates_percent",
    #     datatype="number",
    # ),
    # Column(
    #     name="natural_resources_and_conservation_bachelors_percent", datatype="number"
    # ),
    # Column(name="architecture_bachelors_percent", datatype="number"),
    # Column(name="area_ethnic_and_gender_studies_bachelors_percent", datatype="number"),
    # Column(name="communication_journalism_bachelors_percent", datatype="number"),
    # Column(
    #     name="computer_and_information_sciences_diploma_certificates_percent",
    #     datatype="number",
    # ),
    # Column(
    #     name="computer_and_information_sciences_bachelors_percent", datatype="number"
    # ),
    # Column(name="education_diploma_certificates_percent", datatype="number"),
    # Column(name="education_bachelors_percent", datatype="number"),
    # Column(name="engineering_bachelors_percent", datatype="number"),
    # Column(name="engineering_technologies_bachelors_percent", datatype="number"),
    # Column(
    #     name="foreign_languages_literatures_and_linguistics_bachelors_percent",
    #     datatype="number",
    # ),
    # Column(name="family_and_consumer_sciences_bachelors_percent", datatype="number"),
    # Column(name="english_bachelors_percent", datatype="number"),
    # Column(
    #     name="liberal_arts_general_studies_diploma_certificates_percent",
    #     datatype="number",
    # ),
    # Column(name="liberal_arts_general_studies_bachelors_percent", datatype="number"),
    # Column(name="biological_life_sciences_percentage_1", datatype="number"),
    # Column(name="mathematics_and_statistics_percentage_1", datatype="number"),
    # Column(name="interdisciplinary_studies_percentage_1", datatype="number"),
    # Column(name="interdisciplinary_studies_percentage_2", datatype="number"),
    # Column(name="parks_and_recreation_percentage_1", datatype="number"),
    # Column(name="parks_and_recreation_percentage_2", datatype="number"),
    # Column(name="philosophy_and_religious_studies_percentage_2", datatype="number"),
    # Column(name="physical_sciences_percentage_2", datatype="number"),
    # Column(name="psychology_percentage_2", datatype="number"),
    # Column(name="social_sciences_percentage_1", datatype="number"),
    # Column(name="social_sciences_percentage_2", datatype="number"),
    # Column(name="transportation_and_materials_moving_percentage_2", datatype="number"),
    # Column(name="visual_and_performing_arts_percentage_1", datatype="number"),
    # Column(name="visual_and_performing_arts_percentage_2", datatype="number"),
    # Column(
    #     name="health_professions_and_related_programs_percentage_2", datatype="number"
    # ),
    # Column(name="business_marketing_percentage_1", datatype="number"),
    # Column(name="business_marketing_percentage_2", datatype="number"),
    # Column(name="history_percentage_2", datatype="number"),
    Column(name="initial_2017_cohort_pell_grant_recipients", datatype="number"),
    Column(
        name="initial_2017_cohort_subsidized_stafford_loan_recipients",
        datatype="number",
    ),
    Column(
        name="initial_2017_cohort_no_pell_grant_or_subsized_loan", datatype="number"
    ),
    Column(name="initial_2017_cohort_total", datatype="number"),
    Column(name="not_persist_2017_cohort_total", datatype="number"),
    Column(name="final_2017_cohort_pell_grant_recipients", datatype="number"),
    Column(
        name="final_2017_cohort_subsidized_stafford_loan_recipients", datatype="number"
    ),
    Column(name="final_2017_cohort_no_pell_grant_or_subsized_loan", datatype="number"),
    Column(name="final_2017_cohort_total", datatype="number"),
    Column(name="completed_in_4_years_pell_grant_recipients", datatype="number"),
    Column(
        name="completed_in_4_years_subsidized_stafford_loan_recipients",
        datatype="number",
    ),
    Column(
        name="completed_in_4_years_no_pell_grant_or_subsized_loan", datatype="number"
    ),
    Column(name="completed_in_4_years_total", datatype="number"),
    Column(name="completed_in_5_years_pell_grant_recipients", datatype="number"),
    Column(
        name="completed_in_5_years_subsidized_stafford_loan_recipients",
        datatype="number",
    ),
    Column(
        name="completed_in_5_years_no_pell_grant_or_subsized_loan", datatype="number"
    ),
    Column(name="completed_in_5_years_total", datatype="number"),
    Column(name="completed_in_6_years_pell_grant_recipients", datatype="number"),
    Column(
        name="completed_in_6_years_subsidized_stafford_loan_recipients",
        datatype="number",
    ),
    Column(
        name="completed_in_6_years_no_pell_grant_or_subsized_loan", datatype="number"
    ),
    Column(name="completed_in_6_years_total", datatype="number"),
    Column(
        name="total_graduated_within_6_years_pell_grant_recipients", datatype="number"
    ),
    Column(
        name="total_graduated_within_6_years_subsidized_stafford_loan_recipients",
        datatype="number",
    ),
    Column(
        name="total_graduated_within_6_years_no_pell_grant_or_subsized_loan",
        datatype="number",
    ),
    Column(name="total_graduated_within_6_years_total", datatype="number"),
    Column(
        name="six_year_graduation_rate_2017_cohort_pell_grant_recipients_percent",
        datatype="number",
    ),
    Column(
        name="six_year_graduation_rate_2017_cohort_subsidized_stafford_loan_recipients_percent",
        datatype="number",
    ),
    Column(
        name="six_year_graduation_rate_2017_cohort_no_pell_grant_or_subsized_loan_percent",
        datatype="number",
    ),
    Column(
        name="six_year_graduation_rate_2017_cohort_total_percent", datatype="number"
    ),
    Column(
        name="international_nonresidents_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(
        name="international_nonresidents_degree_seeking_undergraduates",
        datatype="number",
    ),
    Column(name="international_nonresidents_total_undergraduates", datatype="number"),
    Column(
        name="hispanic_latino_degree_seeking_first_time_first_year", datatype="number"
    ),
    Column(name="hispanic_latino_degree_seeking_undergraduates", datatype="number"),
    Column(name="hispanic_latino_total_undergraduates", datatype="number"),
    Column(
        name="black_or_african_american_non_hispanic_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(
        name="black_or_african_american_non_hispanic_degree_seeking_undergraduates",
        datatype="number",
    ),
    Column(
        name="black_or_african_american_non_hispanic_total_undergraduates",
        datatype="number",
    ),
    Column(
        name="white_non_hispanic_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(name="white_non_hispanic_degree_seeking_undergraduates", datatype="number"),
    Column(name="white_non_hispanic_total_undergraduates", datatype="number"),
    Column(
        name="american_indian_or_alaska_native_non_hispanic_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(
        name="american_indian_or_alaska_native_non_hispanic_degree_seeking_undergraduates",
        datatype="number",
    ),
    Column(
        name="american_indian_or_alaska_native_non_hispanic_total_undergraduates",
        datatype="number",
    ),
    Column(
        name="asian_non_hispanic_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(name="asian_non_hispanic_degree_seeking_undergraduates", datatype="number"),
    Column(name="asian_non_hispanic_total_undergraduates", datatype="number"),
    Column(
        name="native_hawaiian_or_other_pacific_islander_non_hispanic_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(
        name="native_hawaiian_or_other_pacific_islander_non_hispanic_degree_seeking_undergraduates",
        datatype="number",
    ),
    Column(
        name="native_hawaiian_or_other_pacific_islander_non_hispanic_total_undergraduates",
        datatype="number",
    ),
    Column(
        name="two_or_more_races_non_hispanic_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(
        name="two_or_more_races_non_hispanic_degree_seeking_undergraduates",
        datatype="number",
    ),
    Column(
        name="two_or_more_races_non_hispanic_total_undergraduates", datatype="number"
    ),
    Column(
        name="race_and_or_ethnicity_unknown_degree_seeking_first_time_first_year",
        datatype="number",
    ),
    Column(
        name="race_and_or_ethnicity_unknown_degree_seeking_undergraduates",
        datatype="number",
    ),
    Column(
        name="race_and_or_ethnicity_unknown_total_undergraduates", datatype="number"
    ),
    Column(name="total_degree_seeking_first_time_first_year", datatype="number"),
    Column(name="total_degree_seeking_undergraduates", datatype="number"),
    Column(name="total_undergraduates", datatype="number"),
    Column(name="degrees_awarded_certificate_diploma", datatype="number"),
    Column(name="degrees_awarded_associates", datatype="number"),
    Column(name="degrees_awarded_bachelors", datatype="number"),
    Column(name="degrees_awarded_post_bachelors", datatype="number"),
    Column(name="degrees_awarded_masters", datatype="number"),
    Column(name="degrees_awarded_post_masters", datatype="number"),
    Column(
        name="degrees_awarded_doctoral_degree_research_scholarship", datatype="number"
    ),
    Column(
        name="degrees_awarded_doctoral_degree_professional_practice", datatype="number"
    ),
    Column(name="degrees_awarded_doctoral_degree_other", datatype="string"),
    Column(
        name="undergraduate_students_degree_seeking_first_time_first_year_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_degree_seeking_first_time_first_year_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_degree_seeking_first_time_first_year_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_degree_seeking_first_time_first_year_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_other_first_year_degree_seeking_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_other_first_year_degree_seeking_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_other_first_year_degree_seeking_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_other_first_year_degree_seeking_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_degree_seeking_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_degree_seeking_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_degree_seeking_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_degree_seeking_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_total_degree_seeking_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_total_degree_seeking_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_total_degree_seeking_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_total_degree_seeking_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_total_degree_seeking_another_gender_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_total_degree_seeking_another_gender_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_credit_courses_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_credit_courses_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_credit_courses_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="undergraduate_students_all_other_credit_courses_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="total_undergraduate_students_men_full_time_enrollment", datatype="number"
    ),
    Column(
        name="total_undergraduate_students_men_part_time_enrollment", datatype="number"
    ),
    Column(
        name="total_undergraduate_students_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="total_undergraduate_students_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="total_undergraduate_students_another_gender_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="total_undergraduate_students_another_gender_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="total_part_time_undergraduate_degree_seeking_students", datatype="number"
    ),
    Column(
        name="total_full_time_undergraduate_degree_seeking_students", datatype="number"
    ),
    Column(name="total_all_undergraduate_degree_seeking_students", datatype="number"),
    Column(name="total_all_undergraduate_students_enrolled", datatype="number"),
    Column(
        name="graduate_students_degree_seeking_first_time_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_degree_seeking_first_time_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_degree_seeking_first_time_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_degree_seeking_first_time_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_degree_seeking_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_degree_seeking_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_degree_seeking_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_degree_seeking_women_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_credit_courses_men_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_credit_courses_men_part_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_credit_courses_women_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="graduate_students_all_other_credit_courses_women_part_time_enrollment",
        datatype="number",
    ),
    Column(name="total_graduate_students_men_full_time_enrollment", datatype="number"),
    Column(name="total_graduate_students_men_part_time_enrollment", datatype="number"),
    Column(
        name="total_graduate_students_women_full_time_enrollment", datatype="number"
    ),
    Column(
        name="total_graduate_students_women_part_time_enrollment", datatype="number"
    ),
    Column(
        name="total_graduate_students_another_gender_full_time_enrollment",
        datatype="number",
    ),
    Column(
        name="total_graduate_students_another_gender_part_time_enrollment",
        datatype="number",
    ),
    Column(name="total_part_time_graduate_degree_seeking_students", datatype="number"),
    Column(name="total_full_time_graduate_degree_seeking_students", datatype="number"),
    Column(name="total_all_graduate_degree_seeking_students", datatype="number"),
    Column(name="total_all_graduate_students_enrolled", datatype="number"),
]


class CDSDataset(BaseModel):
    """Represents a CDS PDF document for a school"""

    id: str
    filename: str
    description: str


class AcceptedApplicantInfo(BaseModel):
    """Represents male and female applicant information"""

    first_year_applied_male: int = Field(
        description="Total first year full time male applicants"
    )
    first_year_applied_female: int = Field(
        description="Total first year full time female applicants"
    )
    first_year_accepted_male: int = Field(
        description="Total first year full time male applicants who were accepted"
    )
    first_year_accepted_female: int = Field(
        description="Total first year full time female applicants who were accepted"
    )
    first_year_enrolled_male: int = Field(
        description="Total first year full time male applicants who enrolled"
    )
    first_year_enrolled_female: int = Field(
        description="Total first year full time female applicants who enrolled"
    )


class ResidencyInfo(BaseModel):
    """residency breakdowns for total applicants, admits, and enrolled students"""

    first_year_applied_in_state: int = Field(
        description="Total number of first year applicants who were in state"
    )
    first_year_applied_out_of_state: int = Field(
        description="Total number of first year applicants who were out of state"
    )
    first_year_applied_international: int = Field(
        description="Total number of first year applicants who were international"
    )
    first_year_accepted_in_state: int = Field(
        description="Total number of first year applicants that were accepted who were in state"
    )
    first_year_accepted_out_of_state: int = Field(
        description="Total number of first year applicants that were accepted who were out of state"
    )
    first_year_accepted_international: int = Field(
        description="Total number of first year applicants that were accepted who were international"
    )
    first_year_enrolled_in_state: int = Field(
        description="Total number of first year students that enrolled who were in state"
    )
    first_year_enrolled_out_of_state: int = Field(
        description="Total number of first year students that enrolled who were out of state"
    )
    first_year_enrolled_international: int = Field(
        description="Total number of first year students that enrolled who were international"
    )


class WaitListInfo(BaseModel):
    """Breakdown of waitlist information for first time first year students"""

    wait_list_size: int = Field(
        description="Total size of admissions wait list", default=0
    )
    wait_list_admitted: int = Field(
        description="Number of students on wait list who were admitted", default=0
    )
    wait_list_ranked: bool = Field(
        description="Whether or not the wait list is ranked", default=0
    )


class AdmissionsRequirementsInfo(BaseModel):
    """Breakdown of class unit requirements for admitted students"""

    # high_school_diploma_ged_required: bool = Field(
    #     description="Whether or not high school diploma or GED is required for admission"
    # )
    # ged_acceped: bool = Field(
    #     description="Whether or not a GED is accepted for admission"
    # )
    english_credits_required: int = Field(
        description="Number of english credits required for admitted applicants",
        default=0,
    )
    english_credits_recommended: int = Field(
        description="Number of english credits recommended for admitted applicants",
        default=4,
    )
    math_credits_required: int = Field(
        description="Number of math credits required for admitted applicants",
        default=0,
    )
    math_credits_recommended: int = Field(
        description="Number of math credits recommended for admitted applicants",
        default=4,
    )
    science_credits_required: int = Field(
        description="Number of science credits required for admitted applicants",
        default=0,
    )
    science_credits_recommended: int = Field(
        description="Number of science credits recommended for admitted applicants",
        default=3,
    )
    social_studies_credits_required: int = Field(
        description="Number of social studies credits required for admitted applicants",
        default=0,
    )
    social_studies_credits_recommended: int = Field(
        description="Number of social studies credits recommended for admitted applicants",
        default=0,
    )
    history_credits_required: int = Field(
        description="Number of history credits recommended for admitted applicants",
        default=0,
    )
    history_credits_recommended: int = Field(
        description="Number of history credits recommended for admitted applicants",
        default=2,
    )
    elective_credits_required: int = Field(
        description="Number of elective credits required for admitted applicants",
        default=0,
    )
    elective_credits_recommended: int = Field(
        description="Number of elective credits recommended for admitted applicants",
        default=0,
    )
    performing_arts_credits_required: int = Field(
        description="Number of performing arts credits required for admitted applicants",
        default=0,
    )
    performing_arts_credits_recommended: int = Field(
        description="Number of performing arts credits recommended for admitted applicants",
        default=0,
    )
    computer_science_credits_required: int = Field(
        description="Number of computer science credits required for admitted applicants",
        default=0,
    )
    computer_science_credits_recommended: int = Field(
        description="Number of computer science credits recommended for admitted applicants",
        default=0,
    )
    performing_arts_credits_required: int = Field(
        description="Number of performing arts credits required for admitted applicants",
        default=0,
    )
    performing_arts_credits_recommended: int = Field(
        description="Number of performing arts credits recommended for admitted applicants",
        default=0,
    )
    foreign_language_credits_required: int = Field(
        description="Number of foreign language credits required for admitted applicants",
        default=0,
    )
    foreign_language_credits_recommended: int = Field(
        description="Number of foreign language credits recommended for admitted applicants",
        default=2,
    )


class AdmissionFactorWeightClass(str, Enum):
    very_important = "very important"
    important = "important"
    considered = "considered"
    not_considered = "not considered"


class AdmissionsFactorWeights(BaseModel):
    """Information about how heavily weighted certain factors are for admission to this institution"""

    class_rank: AdmissionFactorWeightClass = Field(
        description="Importance weighted on class rank"
    )
    gpa: AdmissionFactorWeightClass = Field(description="Importance weighted on gpa")
    standardized_test_score: AdmissionFactorWeightClass = Field(
        description="Importance weighted on standardized test scores"
    )
    essay: AdmissionFactorWeightClass = Field(
        description="Importance weighted on quality of essay"
    )
    interview: AdmissionFactorWeightClass = Field(
        description="Importance weighted on quality of essay"
    )
    extracurriculars: AdmissionFactorWeightClass = Field(
        description="Importance weighted on extracurriculars, volunteer, or work experience"
    )
    first_gen: AdmissionFactorWeightClass = Field(
        description="Importance weighted on being a first generation student"
    )
    alumni: AdmissionFactorWeightClass = Field(
        description="Importance weighted on if the student's parents are alumni"
    )
    residence: AdmissionFactorWeightClass = Field(
        description="Importance weighted on if the student lives out of state"
    )
    religion: AdmissionFactorWeightClass = Field(
        description="Importance weighted on what the student's religion is"
    )


class StandardizedTestScoreInfo(BaseModel):
    """Breakdown of standardized test scores for admitted applicants"""

    sat_act_required: bool = Field(
        description="Are applicants required to submit their SAT or ACT score?"
    )
    sat_accepted: bool = Field(
        description="Is the SAT accepted for admission to this institution?"
    )
    act_accepted: bool = Field(
        description="Is the ACT accepted for admission to this institution?"
    )
    sat_composite_25_percent: int = Field(
        description="25th percentile composite SAT score of admitted applicants"
    )
    sat_composite_50_percent: int = Field(
        description="50th percentile composite SAT score of admitted applicants"
    )
    sat_composite_75_percent: int = Field(
        description="75th percentile composite SAT score of admitted applicants"
    )
    sat_math_25_percent: int = Field(
        description="25th percentile composite SAT math score of admitted applicants"
    )
    sat_math_50_percent: int = Field(
        description="50th percentile composite SAT math score of admitted applicants"
    )
    sat_math_75_percent: int = Field(
        description="75th percentile composite SAT math score of admitted applicants"
    )
    sat_reading_25_percent: int = Field(
        description="25th percentile composite SAT reading score of admitted applicants"
    )
    sat_reading_50_percent: int = Field(
        description="50th percentile composite SAT reading score of admitted applicants"
    )
    sat_reading_75_percent: int = Field(
        description="75th percentile composite SAT reading score of admitted applicants"
    )
    act_composite_25_percent: int = Field(
        description="25th percentile composite ACT score of admitted applicants"
    )
    act_composite_50_percent: int = Field(
        description="50th percentile composite ACT score of admitted applicants"
    )
    act_composite_75_percent: int = Field(
        description="75th percentile composite ACT score of admitted applicants"
    )
    act_math_25_percent: int = Field(
        description="25th percentile composite ACT math score of admitted applicants"
    )
    act_math_50_percent: int = Field(
        description="50th percentile composite ACT math score of admitted applicants"
    )
    act_math_75_percent: int = Field(
        description="75th percentile composite ACT math score of admitted applicants"
    )
    act_english_25_percent: int = Field(
        description="25th percentile composite ACT english score of admitted applicants"
    )
    act_english_50_percent: int = Field(
        description="50th percentile composite ACT english score of admitted applicants"
    )
    act_english_75_percent: int = Field(
        description="75th percentile composite ACT english score of admitted applicants"
    )
    act_writing_25_percent: int = Field(
        description="25th percentile composite ACT writing score of admitted applicants"
    )
    act_writing_50_percent: int = Field(
        description="50th percentile composite ACT writing score of admitted applicants"
    )
    act_writing_75_percent: int = Field(
        description="75th percentile composite ACT writing score of admitted applicants"
    )
    act_science_25_percent: int = Field(
        description="25th percentile composite ACT science score of admitted applicants"
    )
    act_science_50_percent: int = Field(
        description="50th percentile composite ACT science score of admitted applicants"
    )
    act_science_75_percent: int = Field(
        description="75th percentile composite ACT science score of admitted applicants"
    )
    act_reading_25_percent: int = Field(
        description="25th percentile composite ACT reading score of admitted applicants"
    )
    act_reading_50_percent: int = Field(
        description="50th percentile composite ACT reading score of admitted applicants"
    )
    act_reading_75_percent: int = Field(
        description="75th percentile composite ACT reading score of admitted applicants"
    )


class ClassRankInfo(BaseModel):
    """Breakdown of class rank reported by students who were accepted at this institution"""

    top_tenth_percent: float = Field(
        description="Percent of applicants who were in the top tenth of their graduating class"
    )
    top_quarter_percent: float = Field(
        description="Percent of applicants who were in the top quarter of their graduating class"
    )
    top_half_percent: float = Field(
        description="Percent of applicants who were in the top half of their graduating class"
    )
    bottom_half_percent: float = Field(
        description="Percent of applicants who were in the bottom half of their graduating class"
    )
    bottom_quarter_percent: float = Field(
        description="Percent of applicants who were in the bottom quarter of their graduating class"
    )


class GPAInfo(BaseModel):
    """Breakdown of GPA reported by students who were accepted at this institution"""

    average_gpa: float = Field(description="Average GPA of degree seekers")


class ApplicationFees(BaseModel):
    """Breakdown of application fees for this institution"""

    application_fee: float = Field(description="Application fee cost")
    application_fee_waivable: bool = Field(
        description="Can this institution waive the application fee?"
    )


# class ApplicationDueDates(BaseModel):
#     """Breakdown of closing dates for applying to this school"""

#     application_closing_date: Optional[str] = Field(
#         description="Application due date for fall semester"
#     )
#     application_priority_date: Optional[str] = Field(
#         description="Priority date to submit application by"
#     )
#     early_action: bool = Field(description="Does this institution offer early action?")
#     early_action_date: Optional[str] = Field(
#         description="Date to submit application by for early action if offered"
#     )
#     early_decision: bool = Field(
#         description="Does this institution offer early decision?"
#     )
#     early_decision_date: Optional[str] = Field(
#         description="Date to submit application by for early decision if offered"
#     )


# in state tutition
# reciprocity tuition
# religious affiliation tuition
# states with reciprocity
# out of state tuition
# campus housing fees
# campus food fees
# books and supplies fees

# percent of first time freshmen awarded financial aid
# average aid package total
# average scholarship total
# average self help award total
# average need based loan award total

# aid types
# aid deadlines


class InstitutionCDSInfo(BaseModel):
    accepted_applicant_info: AcceptedApplicantInfo = Field(
        description="breakdown of male and female applicants"
    )
    residency_info: ResidencyInfo = Field(
        description="breakdown of where applicants were located"
    )
    # waitlist_info: WaitListInfo = Field(
    #     description="Information about the admissions waitlist"
    # )
    admissions_requirements_info: AdmissionsRequirementsInfo = Field(
        description="Class credit requirements applicants must meet to be elligible for admission"
    )
    # open_admissions_policy: OpenAdmissionsPolicy = Field(
    #     description="Information about this institutions open admissions policy"
    # )
    admissions_factor_weights: AdmissionsFactorWeights = Field(
        description="Information about how heavily weighted application factors are for applicants to this school"
    )
    standardized_test_score_info: StandardizedTestScoreInfo = Field(
        "Breakdown of standardized test scores for admitted students at this institution"
    )
    class_rank_info: ClassRankInfo = Field(
        description="Information about class rank of students at this institution"
    )
    gpa_info: GPAInfo = Field(
        description="Breakdown of GPA scores submitted by applicants who were accepted at this school"
    )
    # fees: ApplicationFees = Field(
    #     description="Breakdown of application fees for this school"
    # )
    # application_due_dates: ApplicationDueDates = Field(
    #     description="Due dates for application to this school"
    # )
