---
layout: post-no-feature
title: "IntroCSExperiencePrediction:---"
description: ""
comments: true
category: articles
---
This is the second part in a series outlining how I determined the leading factors that determine undergraduate introductory Computer Science experience by gender.

<center>
. . .
</center>

<br>


As part of my doctoral study, I decided to investigate the socio-curricular factors that affect the decision to participate in introductory computer science through a data-driven lens. To do this, I designed a research study examining the role of computer science self-identity centered around the experiences of undergraduates in two introductory computer science classes at UC Berkeley.

Once I completed that study, I didn't stop; I decided to ask new questions of the data. Specifically *what were the leading factors that made female students choose intro CS*? With that, the project I titled [IntroCSExperiencePrediction](https://github.com/omoju/IntroCSExperiencePrediction) was born.

To solve this problem, I will undertake the following course of action:   

1. Explore the dataset.   
Usually, I would explore the dataset to ensure its integrity and understand the context. But in this case, I will skip this step since I designed the study and collected the data, I am versed of the context. Further, I have done previous work on this dataset, so I know its boundaries.
2. Identify features that I can potentially use.   
If possible, I should engineer features which might provide greater discrimination of the dataset.
3. With the understanding that this a "classification" task, explore a couple of classifiers that might be well suited for the problem at hand.
4. Select appropriate classifier based on evaluation metric and tune it for optimality.
5. Extract top features responsible for discriminating the data.


### Evaluation Metrics

To evaluate the performance of the classifiers I consider two separate evaluation metrics, the F_1 score of the classifiers and the **expected value**, result. The equation for the expected value is calculated as follows:

![Expected Value]({{ site.url }}/images/CSExperience/expectedValue_equ.png)


The expected value equation, in short, is the expected rates multiplied by the cost-benefit value of each entry in the confusion matrix, weighted by the class priors. I invented a cost and benefits value associated with each entry of the confusion matrix based on domain knowledge. My goal is to reward correct female class classification while penalizing false classifications. My choices for these values can be seen in the image below.

![Cost Benefit Matrix]({{ site.url }}/images/CSExperience/cost_benefit_matrix.png)

Further, the student dataset that I used for this project has unbalanced classes as can be seen in figure. It is important to pay attention to this class unbalance as it can cause the accuracy metric to breakdown as the classes become more skewed.

![Expected Value Calculation]({{ site.url }}/images/CSExperience/expectedValueCalculation.png)



<span style="font-size:0.5em">
Expected rates multiplied by the cost-benefit weighted by the class priors. Image from "Provost and Fawcett. Data Science for Business: What You Need to Know About Data Mining and Data-analytic Thinking, 2013."
</span>

![Target Class]({{ site.url }}/images/CSExperience/targetClass.png)
