# HWRecognizer

The goal of this project is to explore if context specific handwriting recognition models are as performant as the state of the art
generalized handwriting recognition engines available from AWS, Google and Microsoft. Originally the goal was also to test legacy handwriting
engines (ICR) but after brief testing, it was understood that they are only performant on handprint. As our focus is on all handwriting, including
handprint, the legacy engines were excluded from analysis.

The project was divided into 3 main phases:

- Synthetic handwriting generator
- Obtain results for our test set from the available engines (AWS, Microsoft)
- Teaching a crnn model to recognize real human handwriting with only synthetic handwriting provided for training

While AWS, Google and Microsoft have vast resources at their disposal, in the form of both human and financial capital, they are
limited by the need to provide full page OCR/ICR results as part of this service. This leaves the generalized solution at a disadvantage when the 
goal is to read specific fields from a structured form as accurately as possible. 

The HWRecognizer will know the data type of the field which enables it to do two things: 
train a model specifically for that data type and limit the characters expected as output. In contrast, these modern OCR/ICR engines run a 
generalized algorithm which does very well on most machine print and fairly well on handwriting.


## Synthetic Handwriting Generator

The purpose of the synthetic handwriting generator is to create synthetic handwriting snippets which mimic real human handwriting.
The reason for the pursuit of this goal is to generate a large sample size of training and validation snippets which
can be used by a machine learning model. While some real-world sample sets exist, typically the data available focuses on line level (letter format)
handwritten samples which to not translate well for the use case. 

Since the target use case will be structured forms with handwritten
information filled out within specific zones of the document. Because of this, it was important that the generator can control 
the category of text generated, as we will be training different models to understand various categories typically found on 
handwritten forms. Some common examples are Names, Addresses, Dates, ID numbers etc.

## Obtaining Results

For the purposes of comparison, both AWS and Microsoft results were obtained for the test set. These were chosen due to the easy with which we can sign up
for their service and their well-documented API calls which allow us to obtain the required results without large effort.[Microsoft](https://docs.microsoft.com/en-
us/azure/cognitive-services/computer-vision/vision-api-how-to-topics/call-read-api) provides a read ape which supports multiple languages and file formats. [AWS](https://docs.aws.amazon.com/textract/latest/dg/what-is.html) provides two options for testing. The first is the API calls which are simple to implement, but the second
is even easier as a [GUI](https://console.aws.amazon.com/textract/home?region=us-east-1#/demo) interface is available, allowing testing to be done without the need to write any code!

The results from AWS and Microsoft were very good in regard to the test set. For AWS, a WER of 10.6% was achieved and Microsoft was even better with an 8.5% WER. More details
can be found on the [Results](https://github.com/joaopauloucf/HWRecognizer/tree/main/Results) page.


## TF-CRNN Model

All credit to [solivr](https://github.com/solivr/tf-crnn) for this implementation of a Convolutional Recurrent Neural Network (CRNN) for scene text recognition and OCR.
Adapting this for the project, the synthetic handwritten data generated was used as the training and validation sets. Over 35,000 images (500 MB) were used during the training. 
The addition of more data would likely help the model but taking into consideration the cost to deploy an AWS g4dn.xlarge instance and time needed to train
, we believed this to be sufficient. In the future, it may also be beneficial to add both synthetic and real handwriting samples. As mentioned before, this sort of real 
handwriting dataset is lacking for structured forms. With that said, even if the real handwriting samples are line-level(letter) and do not necessarily share the same 
characteristics as handwriting found on a structured document, it may bring diversity to the training set and improve overall performance. We plan on potentially running this 
test in the future.


