Here are some meaningful projects that I have done so far. I'll list brief descriptions for each of the projects down below. Codes in detail can be viewed in corresponding files.
1. Sppech_Graph

This is a simplified Reproduction of the software from paper: Graph analysis of dream reports is especially informative about psychosis. Sci. Rep. 4. It is used for extracting the semantic complexity of any sentences. We used this as a perspective to build up a ML regression model for predicting if the patient has Alzheimer and cognitive impairment. 
Example of a sentence:
<img width="744" alt="image" src="https://github.com/user-attachments/assets/04742aa2-c184-4663-a1aa-3824e7ead80f" />

{'LCC': 30,
 'LSC': 14,
 'degree_average': 2.066666666666667,
 'degree_std': 0.8919392106839769,
 'num_2_cycles': 0,
 'num_3_cycles': 0,
 'number_of_edges': 31,
 'number_of_nodes': 30,
 'number_of_self_loops': 0,
 'reciprocal_edge_pairs': []}
 
 2. CSCI-UA 472 proj1

Wrote two programs that solves the Best Independent Set problem. I used two approaches: The first used iterative deepening; The second used simple hill climbing with random restart.
The “Best Independent Set” problem is defined as follows:
Input: An undirected graph G, in which each vertex is marked by a positive value ;
and a target value T.
Goal: A set of vertices S such that (a) no two vertices in S are connected by an edge
in G; and (b) the total value of the vertices in S is at least T.
For instance, in Graph 1 below, with T = 16, there are three solutions:
{ C,D }, { A,E }, and { B,E }.
In Graph 2, with T = 16 there are two solutions: { G,H,K } and { H,I }.
<img width="573" alt="image" src="https://github.com/user-attachments/assets/1b9db72c-30c5-42f7-804a-784fcdb404da" />

3. CSCI-UA 472 puzzle_solving

Used Davis-Putnam algorithm to to solve a generalization of the 15 puzzle, or sliding puzzle. Specifically, each element of the puzzle is transfered into the propositional calculus and using a SAT-solver.

<img width="224" alt="image" src="https://github.com/user-attachments/assets/2a0e8496-b2f6-4e09-9965-d6d15eeabc4a" />

4. CSCI-UA 472 reinforcement_learning

Used reinforcement learning to learn the correct policy in a Markov Decision Process.The input to the program is a Markov Decision Process. The
program will learn what to do through experimentation with a random restart.

5. CSCI-UA 472 Text_Classification_Naive_Bayes

Used the Na¨ıve Bayes method to build up a classifier for text from training data, and use a test set to evaluate the quality of the classifier. The classifier can based on text descriptions to classify if the person in the text belongs to Government, Music, Writing field.

6. Personal_Health_Consultant_LLM

Build up a full-stack Website: wwww.longevityllmpumc.com.(with Generative AI assiatance). The Website is used for giving personal health recommendation based on the person's vectorized protein expression and basic information. The key technique is front-end and back-end designing, API calling, and Prompt Engineering. The main prediction is based on a ML algorithm, which is not written by me. 

7. RLHF_proj

Used PPO algorithm building up two models(One actor, One critic) for translating a series of number into Capital letter Chinese and Lower case Chinese in terms of numbers. Used GPT-2 as the base model by locally deploy.

8. DL_proj

A really classical image identification, specifically cloth identification, reproduction that I have done to deepen my understanding toward deep learning and how exactly it works on code. Through this project I learned some technical skills on Pytorch.


