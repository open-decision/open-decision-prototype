//Shepherd tour boilerplate
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
                  id: 'start-block-explaination',
                  text: 'Drag this block to the canvas to start building your tree.',
                  attachTo: {
                    element: '#start-block',
                    on: 'bottom'
                  },
                  classes: 'example-step-extra-class ml-5',
                  buttons: [
                    {
                      text: 'Next',
                      action: tour.next
                    }
                  ]
                },
              ];

          tour.addSteps(steps);
          tour.start();
      };
  //Closing of boilerplate
  script.src = staticPath + 'tours/src/shepherd.min.js';
  script.type = 'text/javascript';
  document.head.appendChild(script);
