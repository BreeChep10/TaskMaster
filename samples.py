#new-task-form {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    border-radius: 8px;
    background: linear-gradient(to right, #2bc0e4, #eaecc6);
    box-shadow: rgba(0, 0, 0, 0.15) 0px 10px 15px;
    display: none; /* Hidden by default */
    z-index: 1000;
    position: relative;
    animation: fadeIn 0.5s ease-out;
}

/* Button to show form */
#show-task-form-btn {
    background-color: #1d4350;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 1.2rem;
    margin: 2rem auto;
    display: block;
    outline: none;
}

#show-task-form-btn:hover {
    background-color: #a43931;
}

#close-task-form-btn {
    background-color: #ff4b1f;
    color: #fff;
    padding: 5px 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    margin-bottom: 1rem;
    float: right;
    outline: none;
}

#close-task-form-btn:hover {
    background-color: #1fddff;
}

#show-task-form-btn:focus,
#close-task-form-btn:focus,
.submit-btn:focus {
    outline: 2px solid #ffffff;
    outline-offset: 2px;
}