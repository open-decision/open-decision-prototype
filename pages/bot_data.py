tree = {
  "header": {
    "version": 0.1,
    "build_date": "2020-01-20",
    "logic_type": "jsonLogic version X",
    "owner": "Testperson",
    "tree_name": "R\u00fccklastschriftgeb\u00fchren",
    "tree_slug": "rucklastschriftgebuhren",
    "start_node": "start",
    "vars": {}
  },
  "angemessen": {
    "name": "angemessen",
    "question": "Eine Geb\u00fchr von bis zu vier Euro ist leider angemessen.",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  },
  "ankundigung": {
    "name": "Ank\u00fcndigung",
    "question": "Wurde die Lastschrift vorher durch eine Rechnung angek\u00fcndigt oder zieht die Firma regelm\u00e4\u00dfig Geld ein?",
    "input_type": "button",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "==": [
            {
              "var": "answer"
            },
            "Ja"
          ]
        },
        "0",
        {
          "==": [
            {
              "var": "answer"
            },
            "Nein"
          ]
        },
        "1"
      ]
    },
    "answers": [
      "Ja",
      "Nein"
    ],
    "results": {
      "0": {
        "destination": "ankundigungsart"
      },
      "1": {
        "destination": "musterschreiben"
      }
    }
  },
  "start": {
    "name": "start",
    "question": "<p>Wie hoch sind die von Ihnen geforderten Geb&uuml;hren?</p>",
    "input_type": "number",
    "end_node": "false",
    "rules": {
      "if": [
        {
          ">=": [
            {
              "var": "answer"
            },
            4.0
          ]
        },
        "0",
        {
          "<": [
            {
              "var": "answer"
            },
            4.0
          ]
        },
        "1"
      ]
    },
    "answers": [],
    "results": {
      "0": {
        "destination": "ankundigung"
      },
      "1": {
        "destination": "angemessen"
      }
    }
  },
  "ankundigungsart": {
    "name": "Ank\u00fcndigungsart",
    "question": "<p>Wie wurdest du nach der fehlgeschlagenen Lastschrift benachrichtigt?</p>",
    "input_type": "list",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "in": [
            {
              "var": "answer"
            },
            [
              "E-Mail",
              "Keine Ank\u00fcndigung"
            ]
          ]
        },
        "0",
        {
          "in": [
            {
              "var": "answer"
            },
            [
              "Brief"
            ]
          ]
        },
        "1",
        {
          "in": [
            {
              "var": "answer"
            },
            [
              "SMS"
            ]
          ]
        },
        "2"
      ]
    },
    "answers": [
      "Brief",
      "SMS",
      "E-Mail",
      "Keine Ank\u00fcndigung"
    ],
    "results": {
      "0": {
        "destination": "max3"
      },
      "1": {
        "destination": "max4"
      },
      "2": {
        "destination": "max309"
      }
    }
  },
  "max4": {
    "name": "max4",
    "question": "In diesem Fall ist eine Geb\u00fchr von bis zu vier Euro leider angemessen.",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  },
  "max309": {
    "name": "max3.09",
    "question": "In diesem Fall ist nur eine Geb\u00fchr von 3,09 Euro zul\u00e4ssig. Soll ein Musterschreiben zur R\u00fcckforderung generiert werden?",
    "input_type": "button",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "==": [
            {
              "var": "answer"
            },
            "Ja"
          ]
        },
        "0",
        {
          "==": [
            {
              "var": "answer"
            },
            "Nein"
          ]
        },
        "1"
      ]
    },
    "answers": [
      "Ja",
      "Nein"
    ],
    "results": {
      "0": {
        "destination": "musterschreiben"
      },
      "1": {
        "destination": "ende"
      }
    }
  },
  "max3": {
    "name": "max3",
    "question": "In diesem Fall ist nur eine Geb\u00fchr von 3 Euro zul\u00e4ssig. Soll ein Musterschreiben zur R\u00fcckforderung generiert werden?",
    "input_type": "button",
    "end_node": "false",
    "rules": {
      "if": [
        {
          "==": [
            {
              "var": "answer"
            },
            "Ja"
          ]
        },
        "0",
        {
          "==": [
            {
              "var": "answer"
            },
            "Nein"
          ]
        },
        "1"
      ]
    },
    "answers": [
      "Ja",
      "Nein"
    ],
    "results": {
      "0": {
        "destination": "musterschreiben"
      },
      "1": {
        "destination": "ende"
      }
    }
  },
  "musterschreiben": {
    "name": "Musterschreiben",
    "question": "- Musterschreiben -",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  },
  "ende": {
    "name": "Ende",
    "question": "-",
    "input_type": "button",
    "end_node": "true",
    "rules": {},
    "answers": []
  }
}
