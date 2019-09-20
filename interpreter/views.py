from django.shortcuts import render
# Create your views here.

def show_interpreter(request):
    if request.method == 'GET':
        context = {
        'question': demotree['start']['question'],
        'answers': demotree['start']['answers']
        }
        request.session['last_node'] = 'start'
    elif request.method == 'POST':
        print(request.POST)
        if request.POST.get('restart'):
            context = {
            'question': demotree['start']['question'],
            'answers': demotree['start']['answers']
            }
            request.session['last_node'] = 'start'
        else:
            context = {}
            answer_given = request.POST.get('action')
            print(answer_given)
            try:
                next_node = demotree[request.session['last_node']]['rules'][answer_given]
            except:
                for key in demotree[request.session['last_node']]['rules']:
                    if key.startswith(answer_given):
                        next_node = demotree[request.session['last_node']]['rules'][key]
            context['question'] = demotree[next_node]['question']
            context['answers'] = demotree[next_node]['answers']
            request.session['last_node'] = next_node
    return render(request, 'interpreter.html', context)

demotree = {
'start': {
            'name': 'start',
            'question': 'Willkommen zur Demo-Version des Interpreters. Hier können Sie erfahren, ob die von Ihnen erhobenen Rücklastschriftgebühren berechtigt waren. Die erste Frage: Wie hoch sind die von Ihnen geforderten Gebühren?',
            'answer_type': 'select',
            'answers': ['vier Euro oder weniger', 'mehr als vier Euro'],
            'checks': None,
            'rules': {
            'vier Euro oder weniger': 'angemessen',
            'mehr als vier Euro': 'ankündigung'
            }
          },
'angemessen': {
            'name': 'angemessen',
            'question': 'Eine Gebühr von bis zu vier Euro ist leider angemessen.',
            'answer_type': 'select',
            'answers': [],
            'checks': None,
            'rules': {
            }
          },
'ankündigung': {
            'name': 'Ankündigung',
            'question': 'Wurde die Lastschrift vorher durch eine Rechnung angekündigt oder zieht die Firma regelmäßig Geld ein?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'ankuendigungsart',
            'Nein': 'musterschreiben'
            }
          },
'ankuendigungsart': {
            'name': 'Ankündigungsart',
            'question': 'Wie wurdest du nach der fehlgeschlagenen Lastschrift benachrichtigt?',
            'answer_type': 'select',
            'answers': ['Brief', 'SMS', 'E-Mail', 'garnicht'],
            'checks': None,
            'rules': {
            'Brief': 'max4',
            'SMS': 'max309',
            'E-Mail': 'max3',
            'garnicht': 'max3'
            }
          },
'max4': {
            'name': 'max4',
            'question': 'In diesem Fall ist eine Gebühr von bis zu vier Euro leider angemessen.',
            'answer_type': 'select',
            'answers': [],
            'checks': None,
            'rules': {
            }
          },
'max309': {
            'name': 'max309',
            'question': 'In diesem Fall ist nur eine Gebühr von 3,09 Euro zulässig. Soll ein Musterschreiben zur Rückforderung generiert werden?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'musterschreiben',
            'Nein': 'ende'
            }
          },
'max3': {
            'name': 'max3',
            'question': 'In diesem Fall ist nur eine Gebühr von 3 Euro zulässig. Soll ein Musterschreiben zur Rückforderung generiert werden?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'musterschreiben',
            'Nein': 'ende'
            }
          },
'musterschreiben': {
            'name': 'Musterschreiben',
            'question': 'Hier ein Musterschreiben zur Rückforderung: Die pauschale Absetzung von Rücklastschriftgebühren ist nach ständiger Rspr. jedoch nicht zulässig, lediglich die tatsächlich angefallenen Gebühren sind erstattungsfähig, auch dürfen diese das Interbankengeld von drei Euro nicht erheblich übersteigen (LG Köln, 21.12.2016 - 26 O 331/15;  LG Hamburg, 06.05.2014, 312 O 373/13; OLG S-H, 26.03.2014, 2 U 7/12). Daher widerspreche ich der Zahlung der pauschalen Rücklastschriftgebühr i.H.v. 15€ und bitte um Aufstellung der tatsächlich angefallen Kosten. Gerne überweise ich auch direkt die fehlende Rate  und überweise die angemessenen Rücklastschriftgebühren in einer seperaten Überweisung. Bitte geben Sie mir Bescheid, wenn Sie dies wünschen. Des Weiteren bitte ich darum, auch die folgenden Raten weiterhin per Lastschrift einzuziehen. Sollte aufgrund der fehlgeschlagenen Lastschrift die Neuerteilung eines Mandats nötig sein, bitte ich um Benachrichtigung. Mit freundlichen Grüßen',
            'answer_type': 'select',
            'answers': [],
            'checks': None,
            'rules': {
            }
          },
'ende': {
            'name': 'Ende',
            'question': 'Vielen Dank!',
            'answer_type': 'select',
            'answers': [],
            'checks': None,
            'rules': {
            }
          },
    }


demotreeasyl = {
'start': {
            'name': 'start',
            'question': 'Willkommen zur Demo-Version des Interpreters. Klicke dich durch die Fragen um zu erfahren, ob dein asylsuchender Bewerber bei dir arbeiten darf. Die erste Frage: Hat der Bewerber in Deutschland einen Asylantrag gestellt?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'zwei',
            'Nein': 'end'
            }
          },

'zwei': {
            'name': 'zwei',
            'question': 'Muss der Bewerber im Asylwohnheim leben?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'end',
            'Nein': 'drei'
            }
          },

'drei': {
            'name': 'drei',
            'question': 'Kommt der Bewerber aus der EU oder aus Bosnien-Herzegowina, Mazedonien, Serbien, Montenegro, Albanien, Kosovo, Ghana oder Senegal?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'check_1',
            'Nein': 'vier'
            }
          },
'vier': {
            'name': '',
            'question': 'Wie lange ist der Bewerber schon in Deutschland?',
            'answer_type': 'select',
            'answers': ['Unter drei Monate', 'Drei Monate bis vier Jahre', 'Ueber vier Jahre'],
            'checks': None,
            'rules': {
            'Unter drei Monate': 'end',
            'Drei Monate bis vier Jahre': 'fuenf',
            'Ueber vier Jahre': 'success'
            }
          },
'check_1': {
            'name': 'drei',
            'question': 'Hat der Bewerber seinen Asyalantrag vor dem 31.08.2015 gestellt?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'vier',
            'Nein': 'end'
            }
          },
'fuenf': {
            'name': 'fuenf',
            'question': 'Welche Aufenthaltserlaubnis hat der Bewerber?',
            'answer_type': 'select',
            'answers': ['Arbeitserlaubnis', 'Gestattung', 'Duldung'],
            'checks': None,
            'rules': {
            'Arbeitserlaubnis': 'success',
            'Duldung': 'end',
            'Gestattung' : 'sechs'
            }
          },

'sechs': {
            'name': 'fuenf',
            'question': 'Welche Art von Beschaeftigung wollen Sie anbieten?',
            'answer_type': 'select',
            'answers': ['Praktikum', 'Freiwilligendienst', 'Abhaengige Beschaeftigung'],
            'checks': None,
            'rules': {
            'Praktikum': 'success',
            'Freiwilligendienst': 'success',
            'Abhaengige Beschaeftigung' : 'sieben'
            }
          },
'sieben': {
            'name': 'drei',
            'question': 'Hat der Bewerber einen Hochschulabschluss?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'vier',
            'Nein': 'end'
            }
          },
'acht': {
            'name': 'drei',
            'question': 'Hat der Bewerber einen Hochschulabschluss?',
            'answer_type': 'select',
            'answers': ['Ja', 'Nein'],
            'checks': None,
            'rules': {
            'Ja': 'success',
            'Nein': 'success'
            }
          },
'end': {
            'name': 'drei',
            'question': 'Leider kann der Bewerber nicht arbeiten. Klicke auf Neustart, um von vorne zu beginnen.',
            'answer_type': 'select',
            'answers': [],
            'checks': None,
            'rules': {
            'Ja': 'success',
            'Nein': 'end'
            }
          },
'success': {
            'name': 'drei',
            'question': 'Der Bewerber darf arbeiten! Hier gibt es mehr Informationen. https://immigration-legaltech.herokuapp.com/nineth/results/5/results',
            'answer_type': 'select',
            'answers': [],
            'checks': None,
            'rules': {
            'Ja': 'success',
            'Nein': 'end'
            }
          }
    }
