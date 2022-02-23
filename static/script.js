var sendForm = document.querySelector('#chatform'),
  textInput = document.querySelector('.chatbox'),
  chatList = document.querySelector('.chatlist'),
  userBubble = document.querySelectorAll('.userInput'),
  botBubble = document.querySelectorAll('.bot__output'),
  animateBotBubble = document.querySelectorAll('.bot__input--animation'),
  overview = document.querySelector('.chatbot__overview'),
  hasCorrectInput,
  imgLoader = false,
  animationCounter = 1,
  animationBubbleDelay = 600,
  input,
  previousInput,
  isReaction = false,
  unkwnCommReaction = "무슨 말인지 모르겠어요 : (",
  chatbotButton = document.querySelector(".submit-button")

sendForm.onkeydown = function (e) {
  if (e.keyCode == 13) {
    e.preventDefault();

    //No mix ups with upper and lowercases
    var input = textInput.value.toLowerCase();

    //Empty textarea fix
    if (input.length > 0) {
      createBubble(input)
    }
  }
};

sendForm.addEventListener('submit', function (e) {
  //so form doesnt submit page (no page refresh)
  e.preventDefault();

  //No mix ups with upper and lowercases
  var input = textInput.value.toLowerCase();

  //Empty textarea fix
  if (input.length > 0) {
    createBubble(input)
  }
}) //end of eventlistener

var createBubble = function (input) {
  //create input bubble
  var chatBubble = document.createElement('li');
  chatBubble.classList.add('userInput');

  //adds input of textarea to chatbubble list item
  chatBubble.innerHTML = input;

  //adds chatBubble to chatlist
  chatList.appendChild(chatBubble)

  checkInput(input);
}

var checkInput = function (input) {
  hasCorrectInput = false;
  isReaction = false;
  //Checks all text values in possibleInput
  for (var textVal in possibleInput) {
    //If user reacts with "yes" and the previous input was in textVal
    if (input == 'yes' || input.indexOf('yes') >= 0) {
      if (previousInput == textVal) {
        console.log("sausigheid");

        isReaction = true;
        hasCorrectInput = true;
        botResponse(textVal);
      }
    }
    if (input == 'no' && previousInput == textVal) {
      unkwnCommReaction = "For a list of commands type: Commands";
      unknownCommand("I'm sorry to hear that :(")
      unknownCommand(unkwnCommReaction);
      hasCorrectInput = true;
    }
    //Is a word of the input also in possibleInput object?
    if (input == textVal || input.indexOf(textVal) >= 0 && isReaction == false) {
      console.log("success");
      hasCorrectInput = true;
      botResponse(textVal);

      if (input == "박스오피스") {

      }
    }
  }
  //When input is not in possibleInput
  if (hasCorrectInput == false) {
    //console.log("failed");
    //unknownCommand(unkwnCommReaction);

    requestToServer(input)

    hasCorrectInput = true;
  }
}

function requestToServer(input) {
  $.ajax({
    url: 'http://localhost:5000/question',
    async: true,
    type: 'POST',
    data: JSON.stringify({
      'question': input
    }),
    dataType: 'text',
    contentType: 'application/json; charset=euc-kr',
    success: function (response) {
      botResponse(response)
    },
    error: function (e) {
      botResponse('데이터 처리를 실패했습니다. 관리자에게 문의하세요.')
    }
  })
}

// debugger;

function botResponse(textVal) {
  //sets previous input to that what was called
  // previousInput = input;

  //create response bubble

  var userBubble = document.createElement('li');
  userBubble.classList.add('bot__output');


  if (isReaction == true) {
    if (typeof reactionInput[textVal] === "function") {
      //adds input of textarea to chatbubble list item
      userBubble.innerHTML = reactionInput[textVal]();
    } else {
      userBubble.innerHTML = reactionInput[textVal];
    }
  }

  if (isReaction == false) {
    //Is the command a function?
    if (typeof possibleInput[textVal] === "function") {
      // console.log(possibleInput[textVal] +" is a function");
      //adds input of textarea to chatbubble list item
      userBubble.innerHTML = possibleInput[textVal]();
    } else {
      userBubble.innerHTML = responseText(textVal);
    }
  }
  //add list item to chatlist
  chatList.appendChild(userBubble) //adds chatBubble to chatlist

  // reset text area input
  textInput.value = "";
}

function unknownCommand(unkwnCommReaction) {
  // animationCounter = 1;

  //create response bubble
  var failedResponse = document.createElement('li');

  failedResponse.classList.add('bot__output');
  failedResponse.classList.add('bot__output--failed');

  //Add text to failedResponse
  failedResponse.innerHTML = unkwnCommReaction; //adds input of textarea to chatbubble list item

  //add list item to chatlist
  chatList.appendChild(failedResponse) //adds chatBubble to chatlist

  animateBotOutput();

  // reset text area input
  textInput.value = "";

  //Sets chatlist scroll to bottom
  chatList.scrollTop = chatList.scrollHeight;

  animationCounter = 1;
}

// 답변 기능
function responseText(e) {

  var response = document.createElement('li');

  response.classList.add('bot__output');

  //Adds whatever is given to responseText() to response bubble
  response.innerHTML = e;

  chatList.appendChild(response);

  animateBotOutput();

  //console.log(response.clientHeight);

  //Sets chatlist scroll to bottom
  setTimeout(function () {
    chatList.scrollTop = chatList.scrollHeight;
    //console.log(response.clientHeight);
  }, 0)
}

// 이미지 답변
// function responseImg(e) {
//   var image = new Image();

//   image.classList.add('bot__output');
//   //Custom class for styling
//   image.classList.add('bot__outputImage');
//   //Gets the image
//   image.src = "/images/"+e;
//   chatList.appendChild(image);

//   animateBotOutput()
//   if(image.completed) {
//     chatList.scrollTop = chatList.scrollTop + image.scrollHeight;
//   }
//   else {
//     image.addEventListener('load', function(){
//       chatList.scrollTop = chatList.scrollTop + image.scrollHeight;
//     })
//   }
// }

//change to SCSS loop
function animateBotOutput() {
  chatList.lastElementChild.style.animationDelay = (animationCounter * animationBubbleDelay) + "ms";
  animationCounter++;
  chatList.lastElementChild.style.animationPlayState = "running";
}

function commandReset(e) {
  animationCounter = 1;
  previousInput = Object.keys(possibleInput)[e];
}

// hlep

var possibleInput = {
  // "hlep" : this.help(),
  "help": function () {
    responseText("You can type a command in the chatbox")
    responseText("Something like &quot;Navvy, please show me Mees&rsquo; best work&quot;")
    responseText("Did you find a bug or problem? Tweet me @MeesRttn")
    commandReset(0);
    return
  },
  "박스오피스": function () {
    responseText("I will show you Mees' best work!");
    responseText("These are his <a href='#animation'>best animations</a>")
    responseText("These are his <a href='#projects'>best projects</a>")
    responseText("Would you like to see how I was built? (Yes/No)")
    commandReset(1);
    return
  },
  "영화관 위치": function () {
    responseText("가까운 영화관을 알려드릴게요.");
    responseText("현재 계신 지역을 말씀해주세요.");
    commandReset(2);
    return
  },
  "영화 추천": function () {
    responseText("취향에 맞는 영화를 추천해드려요.");
    responseText("좋아하시는 장르나 감독, 배우를 말씀해주세요.");
    commandReset(3);
    return
  },
  "영화 검색": function () {
    responseText("원하시는 영화의 정보를 알려드릴게요.");
    responseText("장르나 영화 제목을 말씀해주세요.");
    commandReset(4);
    return
  },
  "interests": function () {
    responseText("Mees loves:");
    responseText("Coding complicated chatbots");
    responseText("Family time");
    responseText("Going out with friends");
    responseText("Working out");
    commandReset(5);
    return
  },
  "vision": function () {
    responseText("Things I want to learn or do:");
    responseText("Get great at CSS & JS animation");
    responseText("Create 3D browser experiences");
    responseText("Learn Three.js and WebGL");
    responseText("Combine Motion Design with Front-End");
    commandReset(6);
    return
  },
  "contact": function () {
    responseText("email: <a href='mailto:meesrutten@gmail.com?Subject=Hello%20Mees' target='_top'>send me a message</a>");
    responseText("Twitter: <a href='https://twitter.com/meesrttn'>@MeesRttn</a>");
    commandReset(7);
    return
  },
  "commands": function () {
    responseText("This is a list of commands Navvy knows:")
    responseText("help, best work, about, vision, experience, hobbies / interests, contact, rick roll");
    commandReset(8);
    return
  },
  "rick roll": function () {
    window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  },
  // work experience
}

var reactionInput = {
  "best work": function () {
    //Redirects you to a different page after 3 secs
    responseText("On this GitHub page you'll find everything about Navvy");
    responseText("<a href='https://github.com/meesrutten/chatbot'>Navvy on GitHub</a>")
    animationCounter = 1;
    return
  },
  "about": function () {
    responseText("Things I want to learn or do:");
    responseText("Get great at CSS & JS animation");
    responseText("Create 3D browser experiences");
    responseText("Learn Three.js and WebGL");
    responseText("Combine Motion Design with Front-End");
    animationCounter = 1;
    return
  }
}

// 2022-02-20 추가

$(function () {
  var top10list = ''
  $.ajax({
    url: 'http://localhost:5000/movie/rank',
    async: true,
    type: 'GET',
    dataType: 'json',
    success: function (response) {
      top10list = response

      makeRankBox(top10list)
    },
    error: function (e) {
      botResponse('데이터 처리를 실패했습니다. 관리자에게 문의하세요.')
    }
  })
})

// 2022-02-21 추가
// 박스오피스 탑10 출력
function makeRankBox(top10list) {
  var htmlStr = "";
  htmlStr += "<ul id='rank'>"
  htmlStr += "<li class='rank-item'>- 실시간 박스오피스 -</li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[0]['url'] + "'>1위. " + top10list[0]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[1]['url'] + "'>2위. " + top10list[1]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[2]['url'] + "'>3위. " + top10list[2]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[3]['url'] + "'>4위. " + top10list[3]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[4]['url'] + "'>5위. " + top10list[4]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[5]['url'] + "'>6위. " + top10list[5]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[6]['url'] + "'>7위. " + top10list[6]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[7]['url'] + "'>8위. " + top10list[7]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[8]['url'] + "'>9위. " + top10list[8]['name'] + "</a></li>"
  htmlStr += "<li class='rank-item'><a href='" + top10list[9]['url'] + "'>10위. " + top10list[9]['name'] + "</a></li>"
  htmlStr += "</ul>"
  $(".rank-box").html(htmlStr)

  // 박스오피스를 클릭할 때 이벤트 발생
  $('.rank-box').on({
    "dblclick": function () {
      var ticker = function () {
        timer = setTimeout(function () {
          $('#rank li:first').stop().animate({ marginTop: '-30px' }, 400, function () {
            $(this).detach().appendTo('ul#rank').removeAttr('style');
          });
          ticker();
        }, 2300);
      };
      ticker()
    }

    // "mouseleave": function () {
    //   var ticker = function () {
    //     timer = setTimeout(function () {
    //       $('#rank li:first').stop().animate({ marginTop: '0px' });
    //       ticker();
    //     });
    //   };
    //   ticker()
    // }
  });

  // var ticker = function() {
  //   timer = setTimeout(function() {
  //   $('#rank li:first').animate( {marginTop: '-30px'}, 400, function() {
  //     $(this).detach().appendTo('ul#rank').removeAttr('style');
  //   });
  //   ticker();
  //   }, 2000);         
  // };
  // ticker()

  // 2022-02-20,21 추가
}