@extends('layouts.main')

@section('title', 'Comparing ' . $lang1 . ' and ' . $lang2)

@section('content')
        <div class="container">
            <div class="row mt-5">
                <h2 class="col-12">Comparing {{ $lang1 }}'s and {{ $lang2 }}'s {{ $concept }}</h2>
            </div>
            <div class="row col-12">
                The following will eventually be a table of stuff that's populated with things from the languages
            </div>
            <div class="row">&nbsp;</div>

            <div class="card-group">
                <div class="card">
                    <div class="card-body">
                        <h5 class="text-center">Concept</h5>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h5 class="text-center">{{ $lang1 }}</h5>
                    </div>
                </div>
                <div class="card">
                    <div class="card-body">
                        <h5 class="text-center">{{ $lang2 }}</h5>
                    </div>
                </div>
            </div>

@foreach ($lang1Concepts as $lang1_key => $lang1_value)
    @php
        $lang2_value = $lang2Concepts[$lang1_key];
    @endphp
                <div class="card-group">
                    <div class="card">
                        <div class="card-body">
                            <div class="strong">@php
                            if ($lang1_value["name"] != null) {
                                echo $lang1_value["name"];
                            } else {
                                echo "&nbsp;";
                            }
                            @endphp</div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-body">
                            <div><code>@php
                                        if ($lang1_value["code"] != null) {
                                            echo $lang1_value["code"];
                                        } else {
                                            echo "&nbsp;";
                                        }
                                    @endphp</code></div>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-body">
                            <div><code>@php
                                        if ($lang2_value["code"] != null) {
                                            echo $lang2_value["code"];
                                        } else {
                                            echo "&nbsp;";
                                        }
                                    @endphp</code></div>
                        </div>
                    </div>
                </div>
@endforeach

        </div>

@endsection