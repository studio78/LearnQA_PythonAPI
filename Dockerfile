FROM python
WORKDIR /test_project/
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD python -m pytest -s --alluredir=test_results/ /test_project/tests/