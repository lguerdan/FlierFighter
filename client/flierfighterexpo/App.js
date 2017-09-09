import React, {Component} from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Navigator, NativeModules } from 'react-native';
import { Camera, Permissions } from 'expo';
import { Ionicons } from '@expo/vector-icons';

import { COLOR, ThemeProvider,Button, Toolbar } from 'react-native-material-ui';

const uiTheme = {
    palette: {
        primaryColor: COLOR.green500,
    },
    toolbar: {
      container: {
        height: '10%',
        paddingTop: 25,
      },
    },
    button : {
      container : {
        height : '10%',
        bottom : 0
      }
    }
};

export default class Main extends Component {
    render() {
        return (
            <ThemeProvider uiTheme={uiTheme}>
              <App/>
            </ThemeProvider>
        );
    }
}


class App extends Component {

  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back,
  };

  async componentWillMount() {
   const { status } = await Permissions.askAsync(Permissions.CAMERA);
   this.setState({ hasCameraPermission: status === 'granted' });
  }

  handleTouchableOpacityPress = () => {
    this.setState({
      type: this.state.type === Camera.Constants.Type.back
        ? Camera.Constants.Type.front
        : Camera.Constants.Type.back,
    });
  }

  render(){
    const { hasCameraPermission } = this.state;
    return (
      <View>
        <Toolbar
          leftElement = "menu"
          rightElement = "account-circle"
        />
        <CameraContainer
          hasCameraPermission = {hasCameraPermission}
          handleTouchableOpacityPress = {this.handleTouchableOpacityPress}
          type = {this.state.type}
        />

        <Button primary text="Capture"/>
      </View>
    )
  }
}

class CameraContainer extends Component {
  render(){
    const hasCameraPermission = this.props.hasCameraPermission;
    if (!hasCameraPermission){
      return <View style = {{height : '80%'}} />
    }
    else {

    }
    return(
      <View style = {{height : '80%'}}>
        <Camera
          style={{ flex: 1 }}
          type={this.props.type}
          >
          <View
            style={{
              flex: 1,
              backgroundColor: 'transparent',
              flexDirection: 'row',
            }}>
            <TouchableOpacity
              style={{
                flex: 0.1,
                alignSelf: 'flex-end',
                alignItems: 'center',
              }}
              onPress={() => {
                this.props.handleTouchableOpacityPress();
              }}>
              <Ionicons name="md-reverse-camera" size={32} color="white" style = {{paddingBottom : 10}}/>
            </TouchableOpacity>
          </View>
        </Camera>
      </View>
    )
  }
}
