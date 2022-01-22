from flask import Flask,  request, jsonify, send_file

import torch
import argparse
import code
import prettytable
import logging

from termcolor import colored
from drqa import pipeline
from drqa.retriever import utils

app = Flask(__name__)

STYLE_SHEET = "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.4/css/bulma.css"
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.3.1/js/all.js"
WEB_HTML = """
<html>
    <link rel="stylesheet" href={} />
    <script defer src={}></script>
    <head><title> Interactive Run </title></head>
    <body>
        <div class="columns" style="height: 100%">
            <div class="column is-three-fifths is-offset-one-fifth">
              <section class="hero is-info is-large has-background-light has-text-grey-dark" style="height: 100%">
                <div id="parent" class="hero-body" style="overflow: auto; height: calc(100% - 76px); padding-top: 1em; padding-bottom: 0;">
                    <article class="media">
                      <div class="media-content">
                        <div class="content">
                          <p>
                            <strong>Instructions</strong>
                            <br>
                            Enter a message, and the model will respond interactively.
                          </p>
                        </div>
                      </div>
                    </article>
                </div>
                <div class="hero-foot column is-three-fifths is-offset-one-fifth" style="height: 76px">
                  <form id = "interact">
                      <div class="field is-grouped">
                        <p class="control is-expanded">
                          <input class="input" type="text" id="userIn" placeholder="Type in a message">
                        </p>
                        <p class="control">
                          <button id="respond" type="submit" class="button has-text-white-ter has-background-grey-dark">
                            Submit
                          </button>
                        </p>
                        <p class="control">
                          <button id="restart" type="reset" class="button has-text-white-ter has-background-grey-dark">
                            Restart Conversation
                          </button>
                        </p>
                      </div>
                  </form>
                </div>
              </section>
            </div>
        </div>
        <script>
            function createChatRow(agent, text) {{
                var article = document.createElement("article");
                article.className = "media"
                var figure = document.createElement("figure");
                figure.className = "media-left";
                var span = document.createElement("span");
                span.className = "icon is-large";
                var icon = document.createElement("i");
                icon.className = "fas fas fa-2x" + (agent === "You" ? " fa-user " : agent === "Model" ? " fa-robot" : "");
                var media = document.createElement("div");
                media.className = "media-content";
                var content = document.createElement("div");
                content.className = "content";
                var para = document.createElement("p");
                var paraText = document.createTextNode(text);
                var strong = document.createElement("strong");
                strong.innerHTML = agent;
                var br = document.createElement("br");
                para.appendChild(strong);
                para.appendChild(br);
                para.appendChild(paraText);
                content.appendChild(para);
                media.appendChild(content);
                span.appendChild(icon);
                figure.appendChild(span);
                if (agent !== "Instructions") {{
                    article.appendChild(figure);
                }};
                article.appendChild(media);
                return article;
            }}
            document.getElementById("interact").addEventListener("submit", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;

                console.log(text);
                var data = new FormData();
                data.append( "json",  text  );
                console.log(text);
                fetch('/interact', {{
                    method: 'POST',
                    body: data
                }}).then(response=>response.json()).then(data=>{{
                    console.log(data['data']);
                    var parDiv = document.getElementById("parent");
                    parDiv.append(createChatRow("You", text));
                    // Change info for Model response
                    parDiv.append(createChatRow("Model", data['data']));
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
            document.getElementById("interact").addEventListener("reset", function(event){{
                event.preventDefault()
                var text = document.getElementById("userIn").value;
                document.getElementById('userIn').value = "";
                fetch('/reset', {{
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    method: 'POST',
                }}).then(response=>response.json()).then(data=>{{
                    var parDiv = document.getElementById("parent");
                    parDiv.innerHTML = '';
                    parDiv.append(createChatRow("Instructions", "Enter a message, and the model will respond interactively."));
                    parDiv.scrollTo(0, parDiv.scrollHeight);
                }})
            }});
        </script>
    </body>
</html>
"""

logger = logging.getLogger()
logger.setLevel(logging.INFO)
fmt = logging.Formatter('%(asctime)s: [ %(message)s ]', '%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setFormatter(fmt)
logger.addHandler(console)

parser = argparse.ArgumentParser()
parser.add_argument('--reader-model', type=str, default=None,
                    help='Path to trained Document Reader model')
parser.add_argument('--retriever-model', type=str, default=None,
                    help='Path to Document Retriever model (tfidf)')
parser.add_argument('--doc-db', type=str, default=None,
                    help='Path to Document DB')
parser.add_argument('--tokenizer', type=str, default=None,
                    help=("String option specifying tokenizer type to "
                          "use (e.g. 'corenlp')"))
parser.add_argument('--candidate-file', type=str, default=None,
                    help=("List of candidates to restrict predictions to, "
                          "one candidate per line"))
parser.add_argument('--no-cuda', action='store_true',
                    help="Use CPU only")
parser.add_argument('--gpu', type=int, default=-1,
                    help="Specify GPU device id to use")
args = parser.parse_args()

args.cuda = not args.no_cuda and torch.cuda.is_available()
if args.cuda:
    torch.cuda.set_device(args.gpu)
    logger.info('CUDA enabled (GPU %d)' % args.gpu)
else:
    logger.info('Running on CPU only.')

if args.candidate_file:
    logger.info('Loading candidates from %s' % args.candidate_file)
    candidates = set()
    with open(args.candidate_file) as f:
        for line in f:
            line = utils.normalize(line.strip()).lower()
            candidates.add(line)
    logger.info('Loaded %d candidates.' % len(candidates))
else:
    candidates = None

logger.info('Initializing pipeline...')
DrQA = pipeline.DrQA(
    cuda=args.cuda,
    fixed_candidates=candidates,
    reader_model=args.reader_model,
    ranker_config={'options': {'tfidf_path': args.retriever_model}},
    db_config={'options': {'db_path': args.doc_db}},
    tokenizer=args.tokenizer
)

def process(question, candidates=None, top_n=1, n_docs=5):
    predictions = DrQA.process(
        question, candidates, top_n, n_docs, return_context=True
    )
    table = prettytable.PrettyTable(
        ['Rank', 'Answer', 'Doc', 'Answer Score', 'Doc Score']
    )
    for i, p in enumerate(predictions, 1):
        table.add_row([i, p['span'], p['doc_id'],
                       '%.5g' % p['span_score'],
                       '%.5g' % p['doc_score']])
    print('Top Predictions:')
    print(table)
    print('\nContexts:')
    for p in predictions:
        text = p['context']['text']
        start = p['context']['start']
        end = p['context']['end']
        output = (text[:start] +
                  text[start: end]  +
                  text[end:])
        print('[ Doc = %s ]' % p['doc_id'])
        print(output + '\n')

        return output


@app.route('/')
def index():
    content = WEB_HTML.format(STYLE_SHEET, FONT_AWESOME)

    return content 

@app.route('/interact', methods=["POST","GET"])
def interact():
    _data = request.form

    print(_data)
    return jsonify({"data":process(_data['json'])})
    # process("Who is Hitler ?")

    return _data


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8181,debug=True)