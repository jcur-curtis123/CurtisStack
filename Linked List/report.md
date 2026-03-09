# Report Homework 3 DS 5010

## Coding Reflection

Overall, I felt this assignment was straightforward and clear. I took a bit of time to read through the assignment, and comprehend. 

The more complicated portions to this assignment was the removing of a node on the linked list. This required to reassign the self.head nodes and to move recursively through the linked list.

This assignment I felt served its purpose most effectively. I was able to understand and implement my own linked list, with the additions and proper deductions of nodes. 

I'd be interested to see the difference between a iterative vs recursive filter() function. Meaning, calculate the run time of both and determine what would be most effective (better overall run time).


## Filter Algorithm 

The filter algorithm is a recursive function that takes a lambda as parameter, and of course self. The filter (with given lambda) filters through the linked list, creating a copy of the original list. The function returns the data for the current node, and calls itself for the next_node. This sort of looks like: node(self.data, self.data.filter(lam2)) where lam2 is the parameter, our lambda. 

Filter has a if-else statement that if the current node meets the condition of the lambda, continue with the filter, if not continue through the linked list. 

I've also included a case where the if the node meets the condition for the lambda, continue to filter and if the self.next does not exist, return the current node data and the next node to be None. 




## Self Grade 

For this assignment, I feel that a 90 best demonstrates the effort/skill for this assignment. If I had a little more time, I could have implemented a cleaner way of adding and deleting nodes. I felt that if else statements, and node reassignment was best here. 

I could have added a more in depth recursive function for remove_at_index, as well as 