import streamlit as st
import streamlit.components.v1 as components
import time
st.title('HOSPITAL INFORMATION CENTER')


st.json(st.session_state.json)


#physicians = ["Physician 1", "Physician 2", "Physician 3"]
physician_list = "".join([f"<li>{physician}</li>" for physician in st.session_state.json['Physicians']])
symptoms_list = "".join([f"<li>{symptom}</li>" for symptom in st.session_state.json['Symptoms']])
button_color = {'Emergency':'danger','Non-Emergency':'warning',None:'primary'}

#output = f"<ul>{physician_list}</ul>"
#print(output)


# bootstrap 4 collapse example
components.html(
            f"""
                            <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Interactive Information Box</title>
            <!-- Add Bootstrap CSS link here -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
        
        <!-- Button to trigger the modal -->
        <button type="button" class="btn btn-{button_color[st.session_state.json['Situation']]}" data-toggle="modal" data-target="#infoModal">
            Open Information
        </button>
        
        <!-- Modal -->
        <div class="modal fade" id="infoModal" tabindex="-1" role="dialog" aria-labelledby="infoModalLabel" aria-hidden="true">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="infoModalLabel">Information Box</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <dl class="row">
                            <dt class="col-sm-4">Situation:</dt>
                            <dd class="col-sm-8">{st.session_state.json['Situation']}</dd>
        
                            <dt class="col-sm-4">Age:</dt>
                            <dd class="col-sm-8">{st.session_state.json['Age']}</dd>
        
                            <dt class="col-sm-4">Gender:</dt>
                            <dd class="col-sm-8">{st.session_state.json['Gender']}</dd>
        
                            <dt class="col-sm-4">Surgical Status:</dt>
                            <dd class="col-sm-8">{st.session_state.json['Surgical Status']}</dd>
        
                            <dt class="col-sm-4">Trauma Name:</dt>
                            <dd class="col-sm-8">{st.session_state.json['Trauma Name']}</dd>
        
                            <dt class="col-sm-4">Trauma Desc:</dt>
                            <dd class="col-sm-8">{st.session_state.json['Trauma Description']}</dd>
        
                            <dt class="col-sm-4">Physicians:</dt>
                            <dd class="col-sm-8">
                                <ul>
                                   {physician_list}
                                </ul>
                            </dd>
                            
                             <dt class="col-sm-4">Symptoms:</dt>
                            <dd class="col-sm-8">
                                <ul>
                                   {symptoms_list}
                                </ul>
                            </dd>
                        </dl>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-success">Accept</button>
                        <button type="button" class="btn btn-danger">Reject</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Add Bootstrap JS and jQuery scripts here -->
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>

            """,
            height=600,
        )