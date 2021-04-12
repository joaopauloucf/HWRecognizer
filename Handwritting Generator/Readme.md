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

## Step 1: Overlay Generation - Random Sampling of Metadata, font/size assignment and variable placement of characters

The generator will access a CSV file with all of the possible metadata that it can use to crete the snippet, randomly choosing
one from the list. Once the metadata is chosen, it will then randomly assign a font to use. As part of the original project, 
over 200 .TTF and .OTF fonts were included; more can be added or some can be removed from the FONT folder as needed. Because 
human handwritting is not perfect, our first task in generating syntec handwritting is to add random amounts of Kerning(Horizontal
Displacement) and veritical displacement to each character. 

Sample output from random variable placement:

![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step1.gif "Variable Character Placement")

## Step 2: Underlay Generation - Random Sampling of Labels and Background

Due to the need to create realistic form based handwritten examples, the generator will also have to create labels, lines and borders
which align with realistic real world examples we expect the model to understand. The generator will access the first line of the CSV file,
to choose from all of the possible labels that it can use, randomly choosing from the list. We will also have included 16 machine print fonts which
can be assigned to the label randomly. The generator will also create a border on the image to mimic the borders typically found in a specific zone of 
a structured form. The options are either a line, a box or leave it blank. To mimic poor image quality and sourcing issues, it will also randomly assign 
noise on the entire image in the form of Salt & Pepper degradation.

Sample output from Underlay Generation:

![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step2.gif "Underlay Generation")

## Step 3: Image distortions

Once the Overlay and Underlay functions are complete, the resulting image will be the baseline image used to generate multiple variations via Elastic Distortions,
Shearing, Skewing as well as various Morphological Transformations.

The elastic distortions, shearing and skewing are all generated at the same time resulting in more realistic handwritting examples being generated. The elastic distortion
will mimic on a random basis hand force and altering certain characters. The shearing and skewing will mimic the natural slanting and rotation which can be present as well.

Sample output of same resulting image with various degrees of Elastic Distortions,Shearing and Skewing:

![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step3.gif "Distortions")

The various Morphological Transformation are apply are Erosion, Dilation, Openning(Erosion followed by dilation) and Closing(Dilation followed by Erosion).

Sample output of same resulting image with Morphological Transformations:

Erosion:
![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step4.gif "Erosion")
Dilation:
![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step5.gif "Dilation")
Openning:
![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step6.gif "Openning")
Closing:
![alt text](https://github.com/joaopauloucf/HWRecognizer/blob/main/Supporting/Report_Step7.gif "Closing")





