# substack-automation
Automating substack for fun


## install
Create your virtual environment, clone the repo and execute the following command:
```bash
pip install -r ./requirements.txt
```

## usage
To run the application make sure all of the environment variables are set:
```bash
export SUBSTACK_EMAIL="test@gmail.com"
export SUBSTACK_PASSWOD="something"
export SUBSTACK_PUBLISH_URL="https://codingforfun.substack.com/publish?utm_source=menu"
export SUBSTACK_TITLE="My first automated post"
export SUBSTACK_SUB_TITLE="My first automated post using python and selenium"
echo "My first file\n I hope new lines work\n :D" > message.txt
export SUBSTACK_MESSAGE_FILE="./message.txt"

python main.py
```
