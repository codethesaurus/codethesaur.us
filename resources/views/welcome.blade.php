@extends('layouts.main')

@section('title', 'Welcome')

@section('content')
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
@endsection