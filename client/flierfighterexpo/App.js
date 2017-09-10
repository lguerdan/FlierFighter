import Expo from 'expo';
import React, {Component} from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
  CameraRoll,
  TextInput,
} from 'react-native';
import {Button, COLOR, ThemeProvider } from 'react-native-material-ui';


const GOOGLE_VISION_API = 'AIzaSyAchuzZ-iR_Mswd5WUYFOgck8MRP6AQnM0';
const GOOGLE_VISION_URL = 'https://vision.googleapis.com/v1/images:annotate?key=';
const FLIERFIGHTER_URL ='https://fliers.herokuapp.com/getImage';
const CONFIRM_URL = 'https://fliers.herokuapp.com/confirmation';

const uiTheme = {
    palette: {
        primaryColor: COLOR.green500,
    },
    button: {
        container: {
            height: 50,
        },
    },
};


export default class Main extends Component {
  render() {
        return (
            <ThemeProvider uiTheme={uiTheme}>
                <App />
            </ThemeProvider>
        );
    }
}



class App extends Component {
  state = {
    imageUri : null,
    location: null,
    text : null,
    ORC : false,
    eventDetail : false,
    datetime_from:null,
    datetime_to:null,
    title:null,
    position:null
  }

  render(){
    let imageView = null;
    if (this.state.imageUri){
      imageView = (
        <Image
          style={{ width: 300, height: 300 }}
          source={{ uri: this.state.imageUri }}
        />
      );
    }

    let textView = null;
    if (this.state.text){
      textView = (
        <Text style={{ margin: 5 }}>
          {this.state.text}
        </Text>
      )
    }

    if (this.state.OCR && !this.state.eventDetail){
      this.sendText(this.state.text);
    }

    if (!this.state.eventDetail){
      return(
        <View style = {styles.container}>
          {imageView}
          {textView}
          <TouchableOpacity
            style={{ margin: 5, padding: 5, backgroundColor: '#ddd' }}
            onPress={this.captureImage}>
            <Text>Capture another flier</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={{ margin: 5, padding: 5, backgroundColor: '#ddd' }}
            onPress={this.openImage}>
            <Text>Open Image</Text>
          </TouchableOpacity>
        </View>
      )
    }
    else {
      return (
        <View style = {styles.container}>
          <Text>Please Correct Gathered Info</Text>
          <TextInput
            style={{height: 80, borderColor: 'gray', borderWidth: 1, width: '80%',margin: 10}}
            onChangeText={(title) => this.setState({title})}
            value={this.state.title}
            // multiline = {true}
            returnKeyType = 'done'
          />
          <TextInput
            style={{height: 80, borderColor: 'gray', borderWidth: 1, width: '80%',margin: 10}}
            onChangeText={(location) => this.setState({location})}
            value={this.state.location}
            // multiline = {true}
            returnKeyType = 'done'
          />
          <TextInput
            style={{height: 80, borderColor: 'gray', borderWidth: 1, width: '80%',margin: 10}}
            onChangeText={(datetime_from) => this.setState({datetime_from})}
            value={this.state.datetime_from}
            // multiline = {true}
            returnKeyType = 'done'
          />
          <TextInput
            style={{height: 80, borderColor: 'gray', borderWidth: 1, width: '80%',margin: 10}}
            onChangeText={(datetime_to) => this.setState({datetime_to})}
            value={this.state.datetime_to}
            // multiline = {true}
            returnKeyType = 'done'
          />
          <Button
            onPress={() => this.submitCorrections()}
            text="Submit Corrections"
            primary
            raised
          />
        </View>
      )
    }
  }

  submitCorrections = async () => {
    console.log('go!')
    time = this.HRDtoTImestamp(this.state.datetime_from);
    const response = await fetch(`${CONFIRM_URL}`, {
      method : 'POST',
      headers : {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify({'lat': this.state.position.coords.latitude,'lng': this.state.position.coords.longitude, location : this.state.location, datetime_from : time})
    });
    const result = await response.text();
    console.log('submitted',result);
  }

  componentWillMount = () => {
    this._getLocationAsync();
  }

  _getLocationAsync = async () => {
    let { status } = await Expo.Permissions.askAsync(Expo.Permissions.LOCATION);
    if (status !== 'granted') {
      this.setState({
        errorMessage: 'Permission to access location was denied',
      });
    }

    let position = await Expo.Location.getCurrentPositionAsync({});
    this.setState({ position });
    console.log('position',position)
  };

  timestampToHRD = (ts) => {
    if (ts.length > 0){
      ts = ts.replace(/-/g,'/');
      ts = ts.replace(/T/g,' ');
      ts = ts.slice(0,-10);
    }

    return ts
  }

  HRDtoTImestamp = (ts) => {
    if (ts.length > 0){
      ts = ts.replace('/','-');
      ts = ts.replace('/','-');
      ts = ts.replace(/ /g,'T');
      ts = ts + '.000-07:00'
    }

    return ts
  }

  openImage = async () => {
    const {
      cancelled,
      uri,
      base64
    } = await Expo.ImagePicker.launchImageLibraryAsync({base64 : true});
    if(!cancelled){
      this.setState({
        imageUri : uri,
        text : '(loading...)',
        OCR : false,
      });
    }

    const body = {
      requests:[
        {
          image:{
            content:base64,
          },
          features:[
            {
              type:'TEXT_DETECTION',
              maxResults: 10
            }
          ]
        },
      ],
    };


    const response = await fetch(`${GOOGLE_VISION_URL}${GOOGLE_VISION_API}`, {
      method : 'POST',
      headers : {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
      },
      body: JSON.stringify(body),
    });

    const parsed = await response.json();
    const text = parsed.responses[0]['textAnnotations'][0]['description'].toString();
    this.setState({
      text, OCR : true
    })
    // this.sendText(text)

  }



  captureImage = async () => {
    const {
      cancelled,
      uri,
      base64
    } = await Expo.ImagePicker.launchCameraAsync({base64 : true});
    CameraRoll.saveToCameraRoll(uri);

    if(!cancelled){
      this.setState({
        imageUri : uri,
        text : '(loading...)',
        OCR : false
      });
    }

    const body = {
      requests:[
        {
          image:{
            content:base64,
          },
          features:[
            {
              type:'TEXT_DETECTION',
              maxResults: 10
            }
          ]
        },
      ],
    };

    const response = await fetch(`${GOOGLE_VISION_URL}${GOOGLE_VISION_API}`, {
      method : 'POST',
      headers : {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
      },
      body: JSON.stringify(body),
    });

    const parsed = await response.json();
    const text = parsed.responses[0]['textAnnotations'][0]['description'].toString();
    this.setState({
      text, OCR:true
    })

  }


  sendText = async (text) => {
    console.log('hi')
    const response = await fetch(`${FLIERFIGHTER_URL}`, {
      method : 'POST',
      headers : {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json'
      },
      body: JSON.stringify({'imageData': text})
    });
    const eventDetail = await response.json();
    const {datetime_from,datetime_to,location,title} = {...eventDetail}
    console.log(datetime_from,datetime_to)
    this.setState({eventDetail:true,datetime_from : this.timestampToHRD(datetime_from),datetime_to : this.timestampToHRD(datetime_to),location,title, ORC:false});
    // try {
    //   let eventDetail = await response.json();
    //   // let eventDetail = parsedText.json();
    //   // eventDetail.title = eventDetail.title.replace('\\\"')
    //   this.setState({eventDetail})
    //   // console.log("herokuapp",parsed)
    // } catch(e){
    //   let parsedText = await response.text();
    //   console.log("ERROR:",parsedText,e)
    // }


  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
