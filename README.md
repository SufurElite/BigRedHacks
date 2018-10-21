# Plagiarism Detector
This project - currently a Proof of Concept - is a plagiarism detector that utilises Machine Learning, and it was made for BigRedHacks.
## Why?
Currently, plagiarism detectors rely on direct quotation to catch someone, **but plagiarism _is not_ bound to just quoting without citation!** One of the most common, but hardly combatted, areas of Plagiarism is paying for someone else to write a paper for you. The reason why it's rarely combatted is the difficulty in proving it. _That does not mean, however, that the teacher is unaware_. More often than not, a teacher can tell when a paper has been forged due to the change - even if subtle - of writing style. This was the inspiration for this project. This project aims to act as a tool for teachers to prove that someone has used a forged paper by creating a literary footprint of the student and applying machine learning to determine the similarity (or lackthereof) in the writing style of a new paper. 

## Areas for improvement:
1. Currently, although functioning, some false-positives are produced, which is obviously unacceptable. 
2. The application currently is a desktop application - written in python and C#, a WPF application. Although functioning, I'd like to move the python to a server and have a web-interface for the teachers - removing any need to install python modules, etcetera. 
3. I'd like to implement a RNN (Recurrent Neural Network) so that essays written longer ago are valued less than more recent ones. 
