import React, {Component} from 'react';
import { StyleSheet, Text, View, TouchableOpacity } from 'react-native';
import { Navigator, NativeModules } from 'react-native';

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

  render(){
    return (
      <View>
        <Toolbar
          leftElement = "menu"
          rightElement = "account-circle"
        />
        <CameraContainer/>

        <Button primary text="Capture"/>
      </View>
    )
  }
}

class CameraContainer extends Component {
  render(){
    return(
      <View style = {{height : '80%'}}>
        <Text>
          Camera
        </Text>
      </View>
    )
  }
}
