FROM python:3.9
WORKDIR /Pet_Social
COPY . /Pet_Social
RUN pip install -r requirements.txt
RUN chmod +x /Pet_Social/run.sh
RUN chmod -R 775 /Pet_Social
CMD ["/Pet_Social/run.sh"]
EXPOSE 8000
