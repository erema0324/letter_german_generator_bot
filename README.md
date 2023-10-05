<!DOCTYPE html>
<html>
<head>

</head>
<body>

<h1>Telegram Letter Generator Bot</h1>

<p>This is a Telegram bot that generates letters in German from English, Russian, Farsi and Ukrainian languages based on user input.</p>

<h2>Features</h2>

<ul>
  <li>Generates letters in German from other languages</li>
  <li>Supports letter types like request, complaint, proposal, thanks, cover letter</li>
  <li>Users provide subject, sender name, receiver name as input</li>
  <li>For cover letters, users provide job details like position, education, certificates</li>
  <li>Generated letters can be exported as PDF or Word documents</li>
</ul>

<h2>Usage</h2>

<ol>
  <li>Message the bot on Telegram @mybotname</li>
  <li>Choose source language</li>
  <li>Select the letter type</li>
  <li>Provide requested info like subject, sender, etc</li>
  <li>Bot generates letter in German</li>
  <li>Exports available in PDF and Word formats</li>  
</ol>

<h2>Running the Bot</h2>

<h3>Install dependencies</h3>

<p>Install required packages:</p>

<pre>
<code>
pip install -r requirements.txt
</code>
</pre>

<h3>Configure settings</h3>

<p>In config.py specify your API keys:</p>

<pre>
<code>
TELEGRAM_API_TOKEN = 'YOUR_TELEGRAM_TOKEN'
OPENAI_API_KEY = 'YOUR_OPENAI_KEY' 
</code>
</pre>

<h3>Run the bot</h3>

<p>Run main.py to launch the bot:</p>

<pre>
<code>  
python main.py
</code>
</pre>

<h2>Technologies</h2>

<ul>
  <li>Telegram Bot API</li>
  <li>OpenAI API</li>
  <li>Aiogram</li>
  <li>ReportLab and Python-Docx</li>
  <li>Python</li>
</ul>

<h2>To Do</h2>

<ul>
  <li>Add more languages</li>
  <li>Allow letter preview</li>
  <li>Payment integration</li> 
  <li>User account and bot stats</li>
</ul>

<h2>Contributing</h2>

<p>Contributions welcome! Please open an issue or pull request on Github.</p>

<p>This project does not have an explicit license.</p>

</body>
</html>
