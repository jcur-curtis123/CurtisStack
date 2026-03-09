## 1. Reflection

The coding process for this assignment involved implementing decision tree logic to calculate impurity and identify the best partition for splitting data, using the provided `training_data.csv` file.

**What was easy:**  
- Setting up the data loading process and organizing the dataset into partitions was straightforward once the data structure was clear 
- Implementing the Gini impurity formula itself was also simple, as it only required calculating class probabilities and applying the expression `1 - (p_high² + p_low²)`. This is also similar to the Entropy impurity formula with the expression, `-E i=1^k p_i \ log_2(p_i)`. 

**What was hard:**  
I would say that this was a difficult assignment for me. I had some challenges in the sections as mentioned below. I think the normalization of certain attributes (Age) was the most challenging, and of course any related bugs in accordance to the errors prompted from the normalization of the data.
- Handling the Age attribute with the "ghost" \ufeff in the beginning of the string. Python did not like that Age was formatted this way. This required replacing the '\ufeff' with ""
- Debugging the “division by zero” issue and ensuring the weighted impurity was correctly averaged across partitions was challenging
- Interpreting what the “average key value” represented in relation to impurity took some time to understand — this was the beginning part of part 8. After understanding that we must create a threshold for the partitioned attributes, it became clear that the average numeric key values were the threshold. 

**Purpose of the assignment:**

Yes, this homework assignment demonstrated how impurity measures (like Gini) drive decision tree splitting. It was helpful for the layout in steps, to understand how to build a project with many moving parts.

---

## 2. Optimal Partition Decision

According to the two calculations, the best attribute to split on first was:

> **`OnHypertensionMedication`**

This attribute produced the lowest impurity of 0.0, furthering that this separates the data into homogeneous groups with respect to the target label (High Risk vs. Low Risk).  

---

## Works Cited ##

Cites Used to Understand Material:

https://medium.com/analytics-steps/understanding-the-gini-index-and-information-gain-in-decision-trees-ab4720518ba8

https://towardsdatascience.com/decision-trees-explained-entropy-information-gain-gini-index-ccp-pruning-4d78070db36c/

https://medium.com/data-science/entropy-how-decision-trees-make-decisions-2946b9c18c8


AI Prompt:

"Whats the importance of gini vs entropy in reference to a dataset attributes?" 

This prompt assisted me with clarifying the goal of the output, and the basis of the driver.py

To further elaborate on how this prompt assisted me:

We need to partition the dataset in order to achieve the relative "best" attribute and we do this by calculating each partition's gini and impurity calculations

But in order to do that we need to calculate the probability of the "High Risk" or "Low Risk" labels in our stated partition

But we also need to calculate our weights for the relative partition and here is what this might look like:

weight(i) ​= number of records in partition i​ / total number of records across all partitions

The threshold must also be defined within the partition, this is useful for calculating weights and needed for total impurity for each gini and entropy. This total impurity defines what our best attribute is, as each partition has a associated impurity score

"What is '\uffef'?"

This prompt essentially defined what \uffef and I realized that I did not need this in my dataset ie; not required for post processing purposes

---