# FOR LOCAL DEVELOPMENT

```
# Install the packages
# Make sure to run these in a virtual folder. lol

pip install -r requirements.txt

# Run the Azurite docker container

docker run -p 10000:10000 -p 10001:10001 mcr.microsoft.com/azure-storage/azurite

# Run the local FUNC (LOL)

func start --port 3000
```

Extra reading:

Develop Azure Functions locally using Core Tools

LINK: https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Cisolated-process%2Cnode-v4%2Cpython-v2%2Chttp-trigger%2Ccontainer-apps&pivots=programming-language-python

Deployment

https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code?tabs=node-v4%2Cpython-v2%2Cisolated-process%2Cquick-create&pivots=programming-language-python#create-an-azure-functions-project

https://www.youtube.com/watch?v=lpZCwzYVNpA

OR

Run command

```
func azure functionapp publish <FUNCTION-NAME>
```

Make sure given function name is already setup on Azure with the respective Storage and everything
