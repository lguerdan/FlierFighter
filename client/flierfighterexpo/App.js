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
            height: 75,
            paddingTop: 25,
        },
    },
    button : {
      container : {
        height : 50,
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


        <Button primary text="Capture"/>
      </View>
    )
  }
}



// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     backgroundColor: '#fff',
//     alignItems: 'center',
//     justifyContent: 'center',
//   },
// });
