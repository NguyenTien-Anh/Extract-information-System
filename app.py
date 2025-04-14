import json

import gradio as gr
import pollinations

css = """
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
}

body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background-color: #f3f4f6;
}

.gradio-container {
    width: 1500px;
    margin: 0 auto;
}

.main-header {
    text-align: center;
    color: var(--primary-color);
    font-size: 2.5rem;
    margin: 2rem 0;
    font-weight: bold;
}

.tab-nav {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.input-container {
    background-color: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.custom-button {
    background-color: var(--primary-color) !important;
    color: white !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 6px !important;
    font-weight: 600 !important;
    transition: background-color 0.3s ease !important;
}

.custom-button:hover {
    background-color: var(--secondary-color) !important;
}

.output-box {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 1rem;
}

.gradio-container [data-testid="dataframe"] {
    font-family: 'Segoe UI', Arial, sans-serif;
    margin-top: 1rem;
}

.gradio-container [data-testid="dataframe"] th {
    background-color: var(--primary-color);
    color: white;
    padding: 12px;
    font-weight: 600;
}

.gradio-container [data-testid="dataframe"] td {
    padding: 10px;
    border-bottom: 1px solid #e2e8f0;
}

.gradio-container [data-testid="dataframe"] tr:nth-child(even) {
    background-color: #f8fafc;
}

.gradio-container [data-testid="dataframe"] tr:hover {
    background-color: #e2e8f0;
}

.date-input input {
    padding: 8px 12px;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    font-size: 14px;
}

.date-input input:focus {
    border-color: var(--primary-color);
    outline: none;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
}
"""

id_card_model = pollinations.Text(
    model="openai",
    contextual=True,
    system="You are an expert in extracting information from images of citizen identity card. From a given image,"
           " extract personal information"
           " and return it in JSON format as follows: {\"id\": citizen ID number, \"name\": full name, "
           "\"dob\": date of birth in dd-mm-yyyy format, \"gender\": gender, \"nationality\": nationality, "
           "\"place_of_birth\": place of birth, \"place_of_residence\": current residence, "
           "\"date_of_expiry\": date of expiry}. Note: The output must be in JSON format only, with no "
           "additional "
           "text or explanations. If any field cannot be found, set its value to null."
)

driver_license_model = pollinations.Text(
    model="openai-large",
    contextual=True,
    system="You are an expert in extracting information from images of driver license. From a given image,"
           " extract personal information"
           " and return it in JSON format as follows: {\"id\": driver's license number, \"name\": full name, "
           "\"dob\": date of birth in dd-mm-yyyy format, \"address\": address, "
           "\"date_of_issue\": date of issue, \"class_license\": class license}."
           " Note: The output must be in JSON format only, with no additional text or explanations. "
           "If any field cannot be found, set its value to null."
)

card_visit_model = pollinations.Text(
    model="openai",
    contextual=True,
    system="You are an expert in extracting information from images of card visit. From a given image, extract "
           "personal information"
           " and return it in JSON format as follows: {\"name\": full name, \"company\": company, "
           "\"role\": role, \"contact\": contact phone number, \"email\": email, "
           "\"website\": website, \"address\": address}. "
           "Note: The output must be in JSON format only, with no "
           "additional "
           "text or explanations. If any field cannot be found, set its value to null."
)


def main():
    def extract_id_card_func(image):

        id_card_model.image(
            file=image
        )
        res = id_card_model(
            prompt="Extract information from image",
            encode=True
        )
        res = json.loads(res.response)
        return (res["id"], res["name"], res["dob"], res["gender"], res["nationality"], res["place_of_birth"],
                res["place_of_residence"], res["date_of_expiry"])

    def extract_driver_license_func(image):

        driver_license_model.image(
            file=image
        )
        res = driver_license_model(
            prompt="Extract information from image",
            encode=True
        )
        res = json.loads(res.response)
        return res["id"], res["name"], res["dob"], res["address"], res["date_of_issue"], res["class_license"]

    def extract_card_visit_func(image):

        card_visit_model.image(
            file=image
        )
        res = card_visit_model(
            prompt="Extract information from image",
            encode=True
        )
        res = json.loads(res.response)
        return (res["name"], res["company"], res["role"], res["contact"], res["email"],
                res["website"], res["address"])

    with gr.Blocks(title="Extract information System", css=css) as interface:
        gr.Markdown(
            """
            <div class="main-header">
                Extract information System
            </div>
            """
        )

        with gr.Tabs(elem_classes="tab-nav") as tabs:
            with gr.Tab("Identity card"):
                with gr.Column(elem_classes="input-container"):
                    with gr.Row():
                        with gr.Column():
                            image_input = gr.Image(type='filepath')
                            extract_id_card_btn = gr.Button(
                                "✔️ Extract info",
                                elem_classes="custom-button"
                            )
                        with gr.Column():
                            id = gr.Textbox(
                                label="ID"
                            )
                            name = gr.Textbox(
                                label="Name",
                            )
                            dob = gr.Textbox(
                                label="Date of birth",
                            )
                            gender = gr.Textbox(
                                label="Gender",
                            )
                        with gr.Column():
                            nationality = gr.Textbox(
                                label="Nationality",
                            )
                            place_of_birth = gr.Textbox(
                                label="Place of birth",
                            )
                            place_of_residence = gr.Textbox(
                                label="Place of residence",
                            )
                            date_of_expiry = gr.Textbox(
                                label="Date of expiry",
                            )
                        extract_id_card_btn.click(
                            extract_id_card_func,
                            inputs=[image_input],
                            outputs=[id, name, dob, gender, nationality, place_of_birth, place_of_residence,
                                     date_of_expiry]
                        )

            with gr.Tab("Driver license"):
                with gr.Column(elem_classes="input-container"):
                    with gr.Row():
                        with gr.Column():
                            image_input = gr.Image(type='filepath')
                            extract_driver_license_btn = gr.Button(
                                "✔️ Extract info",
                                elem_classes="custom-button"
                            )
                        with gr.Column():
                            id = gr.Textbox(
                                label="ID"
                            )
                            name = gr.Textbox(
                                label="Name",
                            )
                            dob = gr.Textbox(
                                label="Date of birth",
                            )
                        with gr.Column():
                            address = gr.Textbox(
                                label="Address",
                            )
                            date_of_issue = gr.Textbox(
                                label="Date of issue",
                            )
                            class_license = gr.Textbox(
                                label="Class license",
                            )
                        extract_driver_license_btn.click(
                            extract_driver_license_func,
                            inputs=[image_input],
                            outputs=[id, name, dob, address, date_of_issue, class_license]
                        )

            with gr.Tab("Card visit"):
                with gr.Column(elem_classes="input-container"):
                    with gr.Row():
                        with gr.Column():
                            image_input = gr.Image(type='filepath')
                            extract_card_visit_btn = gr.Button(
                                "✔️ Extract info",
                                elem_classes="custom-button"
                            )
                        with gr.Column():
                            name = gr.Textbox(
                                label="Name",
                            )
                            company = gr.Textbox(
                                label="Company",
                            )
                            role = gr.Textbox(
                                label="Role",
                            )
                            contact = gr.Textbox(
                                label="Contact",
                            )
                        with gr.Column():
                            address = gr.Textbox(
                                label="Address",
                            )
                            email = gr.Textbox(
                                label="Email",
                            )
                            website = gr.Textbox(
                                label="Website",
                            )
                        extract_card_visit_btn.click(
                            extract_card_visit_func,
                            inputs=[image_input],
                            outputs=[name, company, role, contact, email, website, address]
                        )
    interface.launch()


if __name__ == "__main__":
    main()
