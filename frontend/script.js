const questionElement = document.getElementById("question");
const optionsElement = document.getElementById("options");
const resultElement = document.getElementById("result");
const funFactElement = document.getElementById("fun-fact");
const nextButton = document.getElementById("next-button");
const scoreElement = document.getElementById("score");
const questionNumberElement = document.getElementById("question-number");

let questions = [];
let currentQuestion = 0;
let score = 0;

nextButton.disabled = true;

fetch("/questions")
    .then(response => response.json())
    .then(data => {

        questions = data;

        showQuestion();

    });


function showQuestion() {

    const question = questions[currentQuestion];

    questionNumberElement.textContent =
    "Question " + (currentQuestion + 1) + " / " + questions.length;

    questionElement.textContent = question.question;

    optionsElement.innerHTML = "";

    resultElement.textContent = "";

    funFactElement.textContent = "";

    question.options.forEach(function(option) {

        const button = document.createElement("button");

        button.textContent = option;

button.onclick = function() {

    // Prevent clicking this question more than once
    if (button.disabled) {
        return;
    }

    button.disabled = true;

    fetch("/check-answer", {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            question: question.question,
            user_answer: option
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log("Backend response:", result);
        console.log("Fun fact element:", funFactElement);

        resultElement.textContent = result.explanation;

        funFactElement.textContent = result.fun_fact
    ? "🤖 AI Fun Fact: " + result.fun_fact
    : "AI fun fact is unavailable.";

        // Disable all answer buttons
        const allButtons = optionsElement.querySelectorAll("button");

        allButtons.forEach(function(button) {
            button.disabled = true;
        });

        nextButton.disabled = false;

        if (result.correct) {
    score++;
    scoreElement.textContent = "Score: " + score;
}

    });

};

        optionsElement.appendChild(button);

    });
}


nextButton.onclick = function() {

    currentQuestion++;

    if (currentQuestion >= questions.length) {

        questionElement.textContent = "Quiz Finished!";

        optionsElement.innerHTML = "";

        resultElement.textContent =
            "Your score: " + score + "/" + questions.length;

        nextButton.style.display = "none";

        return;
    }

    showQuestion();

};