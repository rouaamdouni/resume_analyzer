import streamlit as st

html_code = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="./web/dashboard.css" />
    <link
      href="https://fonts.googleapis.com/icon?family=Material+Icons"
      rel="stylesheet"
    />
    <link
      rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
    />
    <title>Document</title>
  </head>
  <body>
    <div id="container">
      <!-- header -->
      <nav id="navbar">
        <div id="acc-cont"></div>
        <div id="wel-cont">
          <h1>Hi, Welcome to Job Recommender & Resume Analyzer</h1>
        </div>
        <div id="log-cont"></div>
      </nav>

      <!-- main body -->

      <div id="main-body">
        <div id="left-cont">
          <div id="btn-cont">
            <p>What you want to do</p>
            <button class="regression" onclick="showReg()">User</button>
            <button class="classification" onclick="showClass()">Admin</button>
          </div>
          <div id="content-cont"></div>
        </div>
        <div id="right-cont"></div>
      </div>
    </div>
  </body>
  <script src="./web/dashboard.js"></script>
</html>
"""


