import streamlit as st
import requests
import time

def string_generator(text):
    for word in text.split(' '):
        yield word + " "
        time.sleep(0.1)  # Simulate streaming delay

st.title("File Uploader & API Caller")

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["Create Index", "List Index for RAG", "Chatbot"])

with tab1:
    st.header("Upload Files")
    
    # File uploader
    uploaded_files = st.file_uploader("Upload files", type=None, accept_multiple_files=True)

    # Button to send files to API
    if st.button("Send to API") and uploaded_files:
        st.write("Files uploaded successfully:")
        for file in uploaded_files:
            st.write(f"- {file.name}")
        files = [("files", (file.name, file, file.type)) for file in uploaded_files]
        
        with st.spinner("Sending files to API..."):
            try:
                response = requests.post("http://127.0.0.1:8000/upload", files=files)
                if response.status_code == 200:
                    st.success("Files uploaded successfully!")
                    st.success(f"Index Created with name: {response.json()['folder']}")
                else:
                    st.error(f"Error: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")

with tab2:
    st.header("List Created Indexs")
    st.write("May take time depending on the files uploaded and after that will return the indexces list")
    try:
        response = requests.get("http://127.0.0.1:8000/list")
        if response.status_code == 200:
            response = response.json()
            for index in response['index_names']:
                st.subheader(f"Index: {index}")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Use", key=f"chat_{index}", help="Start a chat", use_container_width=True):
                        st.session_state['index_id'] = index
                        st.session_state['messages'] = []
                        st.success("Files have been selected you can now use chatbot at TAB: 3")
                        st.rerun()
                with col2:
                    if st.button("Delete", key=f"delete_{index}", help="Delete this block", use_container_width=True):
                        response = requests.delete(f"http://127.0.0.1:8000/delete/{index}")
                        if response.status_code == 200:
                            st.success(f'index: {index} deleted.')
                            st.rerun()
                st.write("---")  # Separator
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    
    if st.button('Rerun'):
        st.rerun()

with tab3:
    st.header("Chatbot Page")
    if 'index_id' not in st.session_state or st.session_state['index_id'] is None:
        st.write('Select the index you want to use for chatbot.')
    else:
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = requests.post(f'http://127.0.0.1:8000/chat/{st.session_state["index_id"]}', json={"query": prompt})
                if response.status_code == 200:
                    stream = response.json()['text']
                else:
                    stream = f"Error: {response.status_code}, {response.text}"
                response = st.write_stream(string_generator(stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
        for message in st.session_state.messages[::-2]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])