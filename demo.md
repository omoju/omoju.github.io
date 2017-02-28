---
layout:  post-no-feature
permalink: /demo/index.html
description:  

---
<header class="post-header">
  <hgroup>
    <h1>Receipt.ID</h1>
  </hgroup>
</header>


<center>
<iframe src="https://docs.google.com/presentation/d/1VYUDQdA91KWiy3KkZz4pEE9dJTv-p74N93F0LOH4MGE/embed?start=false&loop=false&delayms=3000" frameborder="0" width="300" height="269" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
</center>
<br/>

What do YouTube, Career Builder, and most restaurants have in common? They all rely on a hierarchical taxonomy to organize items in their area. For example, [YouTube](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36411.pdf) uses a taxonomy to understand automatically which category a video belongs. Similarly, [Career Builder](https://arxiv.org/abs/1606.00917) uses a taxonomy to learn which category a job title belongs.

For my project during my data science fellowship at Insight data science, I consulted for a YC backed company that built accounts payable software for restaurant business. This company has developed an app that allows restaurants to scan in their invoices. From these scanned invoices, the company uses a taxonomy to label items. As their data consultant, I created a model which predicted the node in the taxonomy for any given item.

<figure>
  <img src="{{ site.url }}/images/taxonomic_classification/hc_2.png" style="width: 650px;">
</figure>

From the data files, I built a taxonomy of 2000+ nodes spread over four layers. The dataset had an item’s name, its path from the root to the leaf node as well as some other metadata around pricing. From looking at the problem, it was clear that this was a multi-class, multi-label problem that would have a non-trivial solution.


The current approach used focused exclusively on the item's name, for example, a data point in the dataset would have an object's name as "Straus Yogurt" or "Organic spinach." The first challenge with this approach lay in the fact that the item label was quite short, roughly about four to eight words.  Further, when modifiers like *gluten free*, *organic*, or *pesticide free* wherein the item's label, this added a layer of misinformation causing items like *organic milk* and *organic beer* to be classified in the same class.

I took an entirely different approach. I got inspiration from the approach that Google, used in organizing YouTube videos and decided to shift the unit of analysis from item *name* to the *categories* themselves. My approach combines information from both the text-based labels as well as the item's metadata.

This method achieves two crucial things. First, by focusing on individual categories, each time a new category of item is added to the restaurant domain, instead of having to retrain the classifier on the entire dataset, all we have to do is gather enough data for that category, and train a classifier for it. This way, the approach can scale beautifully as the taxonomy grows. Second, moving the unit of analysis from text labels to categories, it becomes easier to correctly separate "organic cream" and "organic beer."

### Data Preprocessing
For the item labels, I tokenized them, then stemmed them using a Snowball stemmer, after which I used Word2Vec to extract word embeddings from the resulting bag of words. I then used the embeddings to vectorize the item label for each datapoint.

### Text-Based Classifiers     
The aim of moving to a category-based solution is to embed knowledge of the taxonomy into classifiers. To do this, I had to figure out how to get positive and negative samples for each category. For every category node, I decided that itself, as well as all its descendants, were *positive* samples for that class. All other nodes that were neither the categories ancestor(s) or itself were set as *negative* samples.  The figure below gives a visual explanation of selecting category training set. I did this for each category node in the tree that had enough data.

One of the limitations of this method is that most nodes have un-balanced classes. Some more severe than other, especially as you go further down in the tree. There are some classes whose ratio of positive signals is as small as 0.02%. The more granular that subclasses get, the harder it is to classify them. The good news is that one can decide to focus on a few of these classes and use synthetic methods to rebalance the dataset.

<figure>
  <img src="{{ site.url }}/images/taxonomic_classification/hc_5.png" style="width: 450px;">
</figure>
With the training sets done, I vectorized them using a mean embedding vectorizer. For each category, I created an AdaBoost binary classifier. I chose to use the AdaBoost after I experimented with several classifiers like LinearSVM and Decision Trees. I first selected Decision Tree since it outperformed the LinearSVM for this problem. However, I quickly realized my aim was to get predicted probabilities as output for the class instead of simple binary output which the Decision Tree gave. For that reason, I switched to AdaBoost, which is a *boosted* decision tree.

I train each classifier using a k=5 kfold cross-validation scheme. I fitted the resulting classifier and retrieved the predicted probability for each data point in the dataset, which resulted in *k* vectors for *k* categories.

### Engineered Features
In addition to the text-based labels, I also wanted to leverage some insight I got into the data to engineer some features. After some preliminary data exploration, I noticed a  trend; certain types items only occurred at certain levels in the tree. This insight resulted in selecting the tree depth for each item as an additional feature.

I also noticed that several items had the same words as nodes along the tree branch as the items name. I calculated how often these item name matches occurred and turned that into another engineered feature.

### Final Model Architecture
<figure>
  <img src="{{ site.url }}/images/taxonomic_classification/hc_4.png" style="width: 450px;">
</figure>
After training the *k=141* classifiers, I extracted the *k* vectors; I carefully combined them with the engineered features, and the other raw metadata taking care to ensure that I assigned the right probabilities to the right data points in my training set.

#### Labeling
For each data point, I assigned the deepest class node in the tree to which it belonged as its label. For example, an item named "bacon ends" belonged to classes [Food, Meats, Pork]. For such an item, I assigned it is label as "Pork."

I feed these features and labels into a multi-label, multi-class Random Forest classifier. I took 75% of the data for training and 25% for testing. Once again I do a 5 fold cross-validation scheme, fitted the final classifier, and retrieve the predicted classes.

### Result
|Tree Level|mapping|Precision|Recall|Chance|
|---|---|---|---|---|
|One |92% |94% |90% | 25%|
|Two | 66%| 80%| 64%| 7.0%|
|Three | 47%|60% |48% | 2.5%|
|Four|39% |44% |50% |3.0% |          

The value of this method is that I can take a look at the results, determine which individual text-based classifiers have poor results, and optimize and tune that specific classifier. In the case of the chocolate classifier, I see that the minority class is minuscule. To deal with this great imbalance in the data, I synthetically resample it and retrain the classifier.

### Insights
From this project, I learned that certain wines are quite hard to separate for example, Pinot Noir, Cabernet Sauvignon and Sauvignon blanc. Similarly, it's easy for the classifier to conflate butter and olive oil in general; as dairy and oil actually have a lot in common. 
