import Browser
import Html exposing (Html, button, div, span, text, img)
import Html.Events exposing (onClick)
import Html.Attributes exposing (src, class)
import Http
import Json.Decode exposing (Decoder, field, string, list)


main =
  Browser.element 
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }


-- MODEL

type ImageLoadingStatus
    = Failure
    | Loading
    | Success

type alias Model = 
    { images: List String
    , idx: Int
    , status: ImageLoadingStatus
    }

init : () -> ( Model, Cmd Msg )
init _ =
    (Model ["img/1.jpg"] 0 Loading, getImageListFromServer)


-- UPDATE

type Msg = Next | Previous | ReloadImages | GotImages (Result Http.Error (List String))

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Next ->
      ({ model | idx = min ((List.length model.images) - 1) (model.idx + 1) }, Cmd.none)

    Previous ->
      ({ model | idx = max 0 (model.idx - 1) }, Cmd.none)

    ReloadImages ->
      ({ model | status = Loading}, getImageListFromServer)

    GotImages result ->
      case result of
        Ok data ->
          ({ model | images = data, status = Success }, Cmd.none)

        Err _ ->
          ({ model | status = Failure }, Cmd.none)

-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none


-- VIEW

view : Model -> Html Msg
view model =
  div [ class "jumbotron text-center" ]
    [ viewHeadline model
    , div []
        [ viewCurrentImage model ]
    ]

viewHeadline : Model -> Html Msg
viewHeadline model =
  div []
    [ viewButtons model
    , viewInfoLine model
    ]

viewButtons : Model -> Html Msg
viewButtons model =
    div [ class "nav-spacer" ]
        [ button [ onClick Previous, class "btn btn-primary btn-lg nav-spacer" ] [ text "‹" ]
        , button [ onClick Next, class "btn btn-primary btn-lg nav-spacer" ] [ text "›" ]
        , button [ onClick ReloadImages, class "btn btn-primary btn-lg nav-spacer" ] [ text "↵" ]
        ]

viewInfoLine : Model -> Html Msg
viewInfoLine model =
    div [ class "nav-spacer" ]
        [ viewIndexOfImage model
        , viewStatus model
        ]

viewStatus : Model -> Html Msg
viewStatus model =
  case model.status of
    Failure ->
      span [ class "alert alert-danger nav-spacer" ] [ text "Some error occured!" ]

    Loading ->
      span []
        [ span [ class "alert alert-info nav-spacer" ]
            [ text "Loading..."
            , span [ class "spinner-border text-secondary" ] []
            ]
        ]

    Success ->
      span [ class "alert alert-success nav-spacer" ] [ text "Success" ]

viewIndexOfImage : Model -> Html Msg
viewIndexOfImage model =
    span [ class "alert alert-secondary" ] [ text ( "Bild: " ++ (String.fromInt (1 + model.idx)) ++ "/" ++ (String.fromInt (List.length model.images))) ]

viewCurrentImage : Model -> Html Msg
viewCurrentImage model =
  img [ src (getImagePath model) ] []

getImagePath : Model -> String
getImagePath model =
    case (List.head (List.drop model.idx model.images)) of
        Just name -> name
        Nothing -> "" -- maybe better show some default image

getImageListFromServer : Cmd Msg
getImageListFromServer =
  Http.get
    { url = "http://localhost:5000/images"
    , expect = Http.expectJson GotImages imageListDecoder
    }

imageListDecoder : Decoder (List String)
imageListDecoder =
  list string
