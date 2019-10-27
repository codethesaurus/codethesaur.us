<!doctype html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="utf-8">
    <meta name="description" content="Code Thesaurus: A polyglot developer reference tool" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>Code Thesaurus - @yield('title')</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" integrity="sha384-WskhaSGFgHYWDcbwN70/dfYBj47jz9qbsMId/iRN3ewGhXQFZCSftd1LZCfmhktB" crossorigin="anonymous">
    <link href="//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css" rel="stylesheet" />

    <!-- Fonts -->
    <!-- <link href="https://fonts.googleapis.com/css?family=Raleway:100,600" rel="stylesheet" type="text/css"> -->

    <!-- Styles -->
    <link rel="stylesheet" href="/css/app.css" />
</head>
<body>
<header>
    <nav class="navbar navbar-dark navbar-expand-sm bg-blue box-shadow">
        <div class="container d-flex justify-content-between">
            {{-- Title --}}
            <a class="navbar-brand d-flex align-items-center" href="/">Code Thesaurus</a>

            {{-- Hamburger Menu --}}
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggler" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>

        <div class="collapse navbar-collapse" id="navbarToggler">
            {{-- Navigation Menu --}}
            <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
                <li class="nav-item mr-auto">               {{-- add this into class of <li>: active --}}
                    <a class="nav-link" href="/">Home</a>   {{-- add this to inside of <a>:   <span class="sr-only">(current)</span> --}}
                </li>
                <li class="nav-item mr-auto">
                    <a class="nav-link" href="/about/">About</a>
                </li>
            </ul>
        </div>
    </nav>


{{--    --}}
{{--    <div class="navbar navbar-dark bg-blue box-shadow">--}}
{{--        <div class="container d-flex justify-content-between">--}}
{{--            <a href="/" class="navbar-brand d-flex align-items-center">--}}
{{--                <strong>Code Thesaurus</strong>--}}
{{--            </a>--}}

{{--            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">--}}
{{--                <span class="navbar-toggler-icon"></span>--}}
{{--            </button>--}}

{{--            <div class="collapse navbar-collapse" id="navbarSupportedContent">--}}
{{--                <div class="navbar-nav">--}}
{{--                    <a class="nav-item nav-link active" href="#">Home <span class="sr-only">(current)</span></a>--}}
{{--                    <a class="nav-item nav-link" href="/about/">About</a>--}}
{{--                </div>--}}
{{--            </div>--}}
{{--        </div>--}}
{{--    </div>--}}
</header>

<main role="main">
@yield('content')
</main>


<footer class="text-muted">
    <div class="container">
        <p class="float-right">
            <a href="#">Back to top</a>
        </p>
        <p>Made with &#x2764; by Sarah Withee.</p> <!-- x2764 the heart emoji code -->
        <p>Want to help out? Check the project out on <a href="http://github.com/codethesaurus/" target="_blank">GitHub</a>.</p>
    </div>
</footer>

<!--scripts loaded here-->

<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js" integrity="sha384-smHYKdLADwkXOn1EmN1qk/HfnUcbVRZyYmZ4qpPea6sjB/pTJ0euyQp0Mk8ck+5T" crossorigin="anonymous"></script>

<script src="/js/app.js"></script>

</body>
</html>
