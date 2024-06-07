FROM python:3.9
COPY dist/sqlite_api-0.0.1-py3-none-any.whl /root/sqlite_api-0.0.1-py3-none-any.whl
RUN pip install -U pip flask PyYAML xmltodict
RUN pip install /root/sqlite_api-0.0.1-py3-none-any.whl
COPY code/app.py /root/app.py
COPY data/database/my.db /root/my.db
ENV DBPATH /root/my.db
ENV PORT 8080
ENTRYPOINT ["python", "/root/app.py"]
EXPOSE 8080


