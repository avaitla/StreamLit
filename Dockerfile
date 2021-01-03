FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /root/.streamlit
RUN echo '[general]\nemail = "a@a.a"' > /root/.streamlit/credentials.toml

COPY . .

CMD [ "streamlit", "run", "streamlit_test.py", "--server.port", "8080" ]
