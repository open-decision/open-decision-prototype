//Shepherd tour boilerplate
window.StartTour =  function(){
      var staticPath = document.getElementById('static-path').value;
      var link = document.createElement('link');
      link.rel = 'stylesheet';
      link.type = 'text/css';
      link.href = staticPath + 'tours/src/shepherd.css'
      document.head.appendChild(link);

      var script = document.createElement('script');
      script.onload = function () {
//Define tour and steps here
                const tour = new Shepherd.Tour({
                  useModalOverlay: true,
                  defaultStepOptions: {
                    classes: 'shadow-md bg-purple-dark',
                    scrollTo: true,
                  }
                });

                const steps = [{
                  id: 'introduction',
                  text: 'Welcome to Open Decision! Do you want us to give you a quick introduction?',
                  classes: 'example-step-extra-class',
                  buttons: [
                    {
                      action: function() {
                        return this.show('end-of-tour');
                      },
                      secondary: true,
                      text: 'No, I am fine'
                    },
                    {
                      action: function() {
                        return this.next();
                      },
                      text: 'Yes, sure!'
                    }
                  ],
                },


      
                ];

          tour.addSteps(steps);
          tour.start();
  //Edit until here, don't change the code below.
      };
  //Closing of boilerplate
  script.src = staticPath + 'tours/src/shepherd.min.js';
  script.type = 'text/javascript';
  document.head.appendChild(script);
  }
window.StartTour();
