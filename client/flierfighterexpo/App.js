import Expo from 'expo';
import React, {Component} from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Image,
  CameraRoll
} from 'react-native';


const GOOGLE_VISION_API = 'AIzaSyAchuzZ-iR_Mswd5WUYFOgck8MRP6AQnM0';
const GOOGLE_VISION_URL = 'https://vision.googleapis.com/v1/images:annotate?key=';






export default class App extends Component {
  state = {
    imageUri : null,
    text : null,
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

    // if (this.state.imageUri){
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



  openImage = async () => {
    const {
      cancelled,
      uri,
      base64
    } = await Expo.ImagePicker.launchImageLibraryAsync({base64 : true});
    if(!cancelled){
      this.setState({
        imageUri : uri,
        text : '(loading...)'
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
    this.setState({
      text: parsed.responses[0]['textAnnotations'][0]['description']
    })

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
        text : '(loading...)'
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
    this.setState({
      text: parsed.responses[0]['textAnnotations'][0]['description']
    })

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
