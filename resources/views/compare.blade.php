@extends('layouts.main')

@section('title', 'Comparing [lang] and [lang]')

@section('content')
        <div class="container">
            <div class="row">
                <h2 class="col-12">Comparing {{ $lang1 }}'s and {{ $lang2 }}'s {{ $concept }}</h2>
            </div>
            <div class="row col-12">
                The following will eventually be a table of stuff that's populated with things from the languages
            </div>

            <div class="card-group">
                <div class="card">
                    <div class="card-body">
                        <h5>Concept</h5>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h5>{{ $lang1 }}</h5>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h5>{{ $lang2 }}</h5>
                    </div>
                </div>
            </div>

@foreach ($concepts as $concept)
                <div class="card-group">
                    <div class="card">
                        <div class="card-body">
                            <div class="strong">{{ $concept }}</div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-body">
                            <div>{{ $lang1Concepts[$concept] }}</div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-body">
                            <div>{{ $lang2Concepts[$concept] }}</div>
                        </div>
                    </div>
                </div>
@endforeach

        </div>

@endsection