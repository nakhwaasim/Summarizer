# Summarizer
Project Description:  
                     PDF Document Summarization Web Application

The project aims to develop a web application that allows users to upload PDF documents and generate summaries of their contents. The application is built using Flask, a Python web framework, and utilizes various libraries such as PyPDF2, spacy, and mysql.connector.

Key Features and Functionality:

1. User Registration and Login: Users can register an account by providing their name, username, and password. They can then log in using their credentials to access the application's features.

2. PDF Upload and Analysis: Users can upload PDF files through the application's interface. The uploaded files are parsed using PyPDF2 to extract the text content from each page. The extracted text is then passed to the summarizer function for analysis and summarization.

3. Summarization Algorithm: The application uses natural language processing (NLP) techniques, implemented with the spacy library, to analyze the extracted text and generate a summary. The summarizer function calculates word frequency, assigns scores to sentences based on word frequency, and selects the top sentences as the summary.

4. Summary Generation and Display: The generated summary is presented to the user, along with the original text, the length of the original document, and the length of the summary. This information helps users understand the level of compression achieved by the summarization algorithm.

5. User Feedback: The application includes a feedback form where users can provide their name, email, and feedback message. The feedback is stored in a MySQL database, allowing the application administrators to review and respond to user feedback.

6. User Interface and Navigation: The web application provides an intuitive user interface with multiple pages, including a home page, login/register pages, a dashboard, summary page, feedback page, and an about page. Users can navigate between these pages using the application's menu and links.

Potential Applications:

1. Academic and Research: Students and researchers can utilize the web application to summarize research papers, academic articles, or lengthy documents, facilitating efficient literature review and comprehension.

2. Professional and Business: Professionals dealing with reports, contracts, or industry-specific documents can leverage the application to obtain concise summaries for decision-making, knowledge sharing, or presentations.

3. News and Media: Journalists and news agencies can use the application to summarize news articles, press releases, or official documents, enabling faster information gathering and content creation.

4. Legal and Compliance: Lawyers, legal researchers, and compliance officers can extract critical information from legal documents, aiding in case preparation, analysis, or compliance reviews.

The web application offers a convenient and time-saving solution for PDF document summarization, enabling users to quickly extract essential information from lengthy texts. It utilizes NLP techniques to deliver accurate and concise summaries, supporting various domains and user requirements.
