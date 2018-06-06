<!doctype html>
<html lang="{{ app()->getLocale() }}">
    <head>
        <meta charset="utf-8">
        <meta name="description" content="CodeThesaurus: A polyglot developer reference tool" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

        <title>Code Thesaurus</title>

        <!-- Bootstrap -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
        <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" />

        <!-- Fonts -->
        <!-- <link href="https://fonts.googleapis.com/css?family=Raleway:100,600" rel="stylesheet" type="text/css"> -->

        <!-- Styles -->
        <link rel="stylesheet" href="css/app.css" />
    </head>
    <body>
    <header>
        <div class="navbar navbar-dark bg-blue box-shadow">
            <div class="container d-flex justify-content-between">
                <a href="#" class="navbar-brand d-flex align-items-center">
                    <strong>Code Thesaurus</strong>
                </a>
                {{--<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarHeader" aria-controls="navbarHeader" aria-expanded="false" aria-label="Toggle navigation">--}}
                    {{--<span class="navbar-toggler-icon"></span>--}}
                {{--</button>--}}
            </div>
        </div>
    </header>

    <main role="main">

        <section class="jumbotron text-center">
            <div class="container">
                <h1 class="jumbotron-heading">The Polyglot Developer Reference</h1>
                <p class="lead text-muted">Use this tool to compare language components from languages you know and don't know, or just use it as a language reference cheat sheet.</p>
            </div>
        </section>

        <div class="album py-5 bg-light">
            <div class="container">
                <div class="card-deck row">
                    <div class="card col-md-6">
                        <form method="post" action="/compare">
                        <div class="card-block">
                            <h5 class="card-header">
                                Learn a Language
                            </h5>
                            <div class="card-body">
                                <h6 class="card-subtitle mb-2 text-muted">
                                    Compare concepts side-by-side with a language you know and one you don't.
                                </h6>
                                <div class="card-text">
                                    Choose a language concept:
                                </div>
                                <div class="card-text">
                                    <div class="form-group">
                                        <select class="form-control" id="concept" name="concept">
                                            <option>Classes</option>
                                            <option>Data Types</option>
                                            <option>File I/O</option>
                                            <option>Namespaces</option>
                                            <option>Strings</option>
                                            <option>Threads</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="card-text">
                                    Pick a language you know and don't know:
                                </div>
                                <div class="card-text">
                                    <div class="form-group">
                                        <select class="form-control" id="lang1" name="lang1">
                                            <option>C++</option>
                                            <option>Haskell</option>
                                            <option>Java</option>
                                            <option>JavaScript</option>
                                            <option>PHP</option>
                                            <option>Python</option>
                                            <option>Ruby</option>
                                        </select>
                                        <select class="form-control" id="lang2" name="lang2">
                                            <option>C++</option>
                                            <option>Haskell</option>
                                            <option>Java</option>
                                            <option>JavaScript</option>
                                            <option>PHP</option>
                                            <option>Python</option>
                                            <option>Ruby</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary">Go!</button>
                                </div>
                            </div>
                        </div>
                        </form>
                    </div>
                    <div class="card col-md-6">
                        <form method="post" action="/cheatsheet">
                        <div class="card-block">
                            <h5 class="card-header">
                                See a Cheat Sheet
                            </h5>
                            <div class="card-body">
                                <h6 class="card-subtitle mb-2 text-muted">
                                    A quick and easy way to remind yourself how to do something.
                                </h6>
                                <div class="card-text">
                                    Choose a language concept:
                                </div>
                                <div class="card-text">
                                    <select class="form-control" id="concept" name="concept">
                                        <option>Classes</option>
                                        <option>Data Types</option>
                                        <option>File I/O</option>
                                        <option>Namespaces</option>
                                        <option>Strings</option>
                                        <option>Threads</option>
                                    </select>
                                </div>
                                <div class="card-text">
                                    Pick a language:
                                </div>
                                <div class="card-text">
                                    <select class="form-control" id="lang1" name="lang1">
                                        <option>C++</option>
                                        <option>Haskell</option>
                                        <option>Java</option>
                                        <option>JavaScript</option>
                                        <option>PHP</option>
                                        <option>Python</option>
                                        <option>Ruby</option>
                                    </select>
                                </div>
                            </div>
                            <div class="card-footer">
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary">Go!</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </main>


    <footer class="text-muted">
        <div class="container">
            <p class="float-right">
                <a href="#">Back to top</a>
            </p>
            <p>Made with &#x2764; by Sarah Withee.</p>
            <p>Want to help out? Check the project out on <a href="http://github.com/codethesaurus/" target="_blank">GitHub</a>.</p>
        </div>
    </footer>

    <!--scripts loaded here-->

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js" integrity="sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T" crossorigin="anonymous"></script>

    <script src="js/app.js"></script>

    </body>
</html>
