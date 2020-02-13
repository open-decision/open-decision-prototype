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
                  id: 'dashboard-link',
                  text: 'This is where you find all your decision trees.',
                  attachTo: {
                    element: '#dashboard-link',
                    on: 'bottom'
                  },
                  classes: 'example-step-extra-class',
                  buttons: [
                    {
                      text: 'Next',
                      action: tour.next
                    }
                  ]
                },
                {
                  id: 'published-link',
                  text: 'On this page you can controll your published trees.',
                  attachTo: {
                    element: '#published-link',
                    on: 'bottom'
                  },
                  classes: 'example-step-extra-class',
                  buttons: [
                    {
                      text: 'Next',
                      action: tour.next
                    }
                  ]
                },
                {
                  id: 'visualbuilder-link',
                  text: 'Wanna try something cool? Head over to our Visualbuilder - but be aware, its still undergoing constructions.',
                  attachTo: {
                    element: '#visualbuilder-link',
                    on: 'bottom'
                  },
                  classes: 'example-step-extra-class',
                  buttons: [
                    {
                      text: 'Next',
                      action: tour.next
                    }
                  ]
                },
                {
                  id: 'tree-name-form',
                  text: 'Enter a name for your new tree and click the button to get started.',
                  attachTo: {
                    element: '#id_name',
                    on: 'bottom'
                  },
                  classes: 'example-step-extra-class',
                  buttons: [
                    {
                      text: 'Next',
                      action: tour.next
                    }
                  ]
                }];

          tour.addSteps(steps);
          tour.start();
      };
  //Closing of boilerplate
  script.src = staticPath + 'tours/src/shepherd.min.js';
  script.type = 'text/javascript';
  document.head.appendChild(script);
