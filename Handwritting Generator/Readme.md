### Setup Instructions ###

* Download all contents within Handwritting Generator onto your local machine
* Install all python packages that are required(requirements.txt)
* Modify OUTPUT, FONT and LABEL file paths within the Config.ini to represent their location on your local machine
* Modify InputPath within the Config.ini to represent their location on your machine
* Modify any other Config.ini settings to achieve desired output


### Handwritting Generator Summary ###

The goal of the handwritting generator is to create synthtic handwritting snippets which mimic real human handwritting.
The reason for our persuit of this goal is to generate a large sample size of training and validation snippets which
we can use in our machine learning model. While some real world sample sets exist, they typically focus on line level(letter format)
handwritten samples which to not translate well for our use case. Our target use case will be stuctured forms with handwritten
information filled out within specific zones of the document. Because of this, it was important that our generator can control 
the category of text generated,as we will be training different models to understand various categories typically found on 
handwritten forms, think along the lines of Names, Addresses, Dates, ID numbers etc. 

## Step 1: Random Sampling of Metadata, font/size assignment and variable placement of characters

The generator will access a CSV file with all of the possible metadata that it can use to crete the snippet, randomly choosing
one from the list. Once the metadata is chosen, it will then randomly assign a font to use. As part of the original project, 
over 200 .TTF and .OTF fonts were included; more can be added or some can be removed from the FONT folder as needed. Because 
human handwritting is not perfect, our first task in generating syntec handwritting is to add random amounts of Kerning(Horizontal
Displacement) and veritical displacement to each character. 

![alt text]("https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step1.gif")


