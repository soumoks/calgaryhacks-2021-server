![Screen Shot 2021-02-14 at 10 10 07 AM](https://user-images.githubusercontent.com/10564697/110074277-2c52cb80-7d3e-11eb-91ef-4cf3215cb227.png)
### Steps to deploy and update the application using AWS SAM.

* Upload the Open API template to s3
```
aws s3 cp openapi.yaml s3://calgaryhacks2021/swagger-template/openapi.yaml --profile personal
```

The above OpenAPI template is referenced inside the sam template, `sam_template.yaml`.
```
DefinitionBody:
          'Fn::Transform':
            Name: 'AWS::Include'
            Parameters:
              Location: s3://calgaryhacks2021/swagger-template/openapi.yaml
```

Update accordingly.

* Build the application
```
sam build --use-container -t sam_template.yml
```

* Package the application
```
sam package --output-template-file packaged.yaml --s3-bucket calgaryhacks2021 --s3-prefix build-artifacts --profile personal
```

* Deploy
```
sam deploy --template-file packaged.yaml --stack-name calgaryhacks2021-api --capabilities CAPABILITY_NAMED_IAM --region us-east-1 --profile personal
```
