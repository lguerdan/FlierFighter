import {
  Camera,
  Video,
  FileSystem,
  Permissions,
} from 'expo';
import React, {Component} from 'react';
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  Slider,
  Image,
  Picker,
  ScrollView,
  Vibration,
} from 'react-native';
import { COLOR, ThemeProvider,Button,Dialog, DialogDefaultActions } from 'react-native-material-ui';

import GalleryScreen from './components/GalleryScreen';

const uiTheme = {
    palette: {
        primaryColor: COLOR.green600,
        secondaryColor : COLOR.amber600
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
    },
    dialog : {
      container: {
        height: '70%',
        width : '70%',
        marginLeft:  '15%',
        marginTop: '35%'
      }
    },
};


const flashModeOrder = {
  off: 'on',
  on: 'auto',
  auto: 'torch',
  torch: 'off',
};

const wbOrder = {
  auto: 'sunny',
  sunny: 'cloudy',
  cloudy: 'shadow',
  shadow: 'fluorescent',
  fluorescent: 'incandescent',
  incandescent: 'auto',
};

class SubmitButton extends Component {

  render(){
    const {onPress} = {...this.props};
    return(
      <Button raised primary
        text="Capture"
        onPress = {() => onPress()}
      />
    )

  }
}

class App extends Component {
  state = {
    flash: 'off',
    zoom: 0,
    autoFocus: 'on',
    depth: 0,
    data : null,
    type: 'back',
    whiteBalance: 'auto',
    ratio: '16:9',
    ratios: [],
    showGallery: false,
    photos: [],
    deletePhoto : {
      enabled : false,
      fileName : null
    },
    pictureTaken : false
  };

  componentDidMount() {
    FileSystem.makeDirectoryAsync(
      FileSystem.documentDirectory + 'photos'
    ).catch(e => {
      FileSystem.readDirectoryAsync(
        FileSystem.documentDirectory + 'photos'
      ).then(photos => {
        this.updatePhotos(photos)
      });
    });
  }

  getRatios = async function() {
    const ratios = await this.camera.getSupportedRatios();
    return ratios;
  };

  updatePhotos = (photos) => {
    this.setState({photos})
  }

  toggleView() {
    this.setState({
      showGallery: !this.state.showGallery,
    });
  }

  toggleFacing = () => {
    this.setState({
      type: this.state.type === 'back' ? 'front' : 'back',
    });
  }

  toggleFlash = () => {
    this.setState({
      flash: flashModeOrder[this.state.flash],
    });
  }

  setRatio(ratio) {
    this.setState({
      ratio,
    });
  }

  toggleWB = () => {
    this.setState({
      whiteBalance: wbOrder[this.state.whiteBalance],
    });
  }

  toggleFocus = () => {
    this.setState({
      autoFocus: this.state.autoFocus === 'on' ? 'off' : 'on',
    });
  }

  zoomOut = () => {
    this.setState({
      zoom: this.state.zoom - 0.1 < 0 ? 0 : this.state.zoom - 0.1,
    });
  }

  zoomIn = () => {
    this.setState({
      zoom: this.state.zoom + 0.1 > 1 ? 1 : this.state.zoom + 0.1,
    });
  }

  setFocusDepth = (depth) => {
    this.setState({
      depth,
    });
  }

  confirmPicture = (data) => {
    this.setState({pictureTaken : true,data});
  }

  savePicture = (data) => {
    const re = /[a-z0-9]*[-][a-z0-9]*[-][a-z0-9]*[-][a-z0-9]*[-][a-z0-9]*.jpg/
    const name = re.exec(data)[0]
    FileSystem.moveAsync({
      from: data,
      to: `${FileSystem.documentDirectory}photos/Photo_${name}`,
    }).then(() => Vibration.vibrate());
  }



  takePicture = async function() {
    if (this.camera) {
      this.camera.takePictureAsync().then(data => this.confirmPicture(data));
    }
  };
  // takePicture = async function() {
  //   if (this.camera) {
  //     this.camera.takePictureAsync().then(data => {
  //       FileSystem.moveAsync({
  //         from: data,
  //         to: `${FileSystem.documentDirectory}photos/Photo_${this.state
  //           .photoId}.jpg`,
  //       }).then(() => {
  //         const photoId = this.state.photoId + 1;
  //         this.setState({
  //           photoId
  //         });
  //         Vibration.vibrate();
  //       });
  //     });
  //   }
  // };

  selectFileToDelete = (photoUri) => {

    const deletePhoto = {
      enabled : photoUri !== null ? true : false,
      fileName : photoUri
    }
    this.setState({deletePhoto});
  }

  deleteFile = (uri) => {
    const filePath = `${FileSystem.documentDirectory}photos/${uri}`;
    const photos = this.state.photos.filter((photo) =>{
      return photo !== uri;
    })
    const deletePhoto = {
      enabled : false,
      fileName : null
    }
    Expo.FileSystem.deleteAsync(filePath,{idempotent:true});

    this.setState({photos,deletePhoto})
  }

  renderGallery() {
    return <GalleryScreen
      onPress={this.toggleView.bind(this)}
      updatePhotos = {this.updatePhotos}
      photos = {this.state.photos}
      onLongPress = {this.selectFileToDelete}
      deletePhotoInfo = {this.state.deletePhoto}
      deleteFile = {this.deleteFile}
    />;
  }

  renderCamera() {
    return (
      <Camera
        ref={ref => {
          this.camera = ref;
        }}
        style={{
          flex: 1,
        }}
        type={this.state.type}
        flashMode={this.state.flash}
        autoFocus={this.state.autoFocus}
        zoom={this.state.zoom}
        whiteBalance={this.state.whiteBalance}
        ratio={this.state.ratio}
        focusDepth={this.state.depth}>
        <View
          style={{
            flex: 0.5,
            backgroundColor: 'transparent',
            flexDirection: 'row',
          }}>
          {/* <TouchableOpacity
            style={styles.flipButton}
            onPress={ () => this.toggleFacing()}>
            <Text style={styles.flipText}> FLIP </Text>
          </TouchableOpacity> */}
          <TouchableOpacity
            style={[
              styles.topRow,
              styles.flipButton,
              styles.galleryButton,
            ]}
            onPress={this.toggleView.bind(this)}>
            <Text style={styles.flipText}> Photos </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.topRow, styles.flipButton]}
            onPress={() => this.toggleFlash()}>
            <Text style={styles.flipText}>
              {' '}FLASH: {this.state.flash}{' '}
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.topRow,styles.flipButton]}
            onPress={() => this.toggleWB()}>
            <Text style={styles.flipText}>
              {' '}WB: {this.state.whiteBalance}{' '}
            </Text>
          </TouchableOpacity>
        </View>
        <View
          style={{
            flex: 0.4,
            backgroundColor: 'transparent',
            flexDirection: 'row',
            alignSelf: 'flex-end',
          }}>
          <Slider
            style={{ width: 150, marginTop: 15, alignSelf: 'flex-end' }}
            onValueChange={(depth) => this.setFocusDepth(depth)}
            value={this.state.depth}
            step={0.1}
            disabled={this.state.autoFocus === 'on'}
          />
        </View>
        <View
          style={{
            flex: 0.1,
            backgroundColor: 'transparent',
            flexDirection: 'row',
            alignSelf: 'flex-end',
          }}>
          <TouchableOpacity
            style={[styles.flipButton, { flex: 0.2, alignSelf: 'flex-end' }]}
            onPress={ () => this.toggleFacing()}>
            <Text style={styles.flipText}> FLIP </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.flipButton, { flex: 0.1, alignSelf: 'flex-end' }]}
            onPress={() => this.zoomIn()}>
            <Text style={styles.flipText}> + </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.flipButton, { flex: 0.1, alignSelf: 'flex-end' }]}
            onPress={() => this.zoomOut()}>
            <Text style={styles.flipText}> - </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.flipButton, { flex: 0.25, alignSelf: 'flex-end' }]}
            onPress={() => this.toggleFocus()}>
            <Text style={styles.flipText}>
              {' '}AF : {this.state.autoFocus}{' '}
            </Text>
          </TouchableOpacity>

        </View>
        <SubmitButton onPress = {this.takePicture.bind(this)} />
      </Camera>
    );
  }

  renderDialog = () => {
    return (
      <Dialog>
        <Dialog.Title><Text>Confirm Picture</Text></Dialog.Title>
        <Dialog.Content>
          <Image
            style={styles.picture}
            source={{
              uri: `${this.state.data}`,
            }}
            key={this.state.data}
          />
        </Dialog.Content>
        {/* <Dialog.Actions>
          <DialogDefaultActions
            style = {{container : {height : 10}}}
             actions={['Discard', 'Keep']}
             onActionPress={(event) => {
               if (event === 'keep'){
                   this.savePicture(this.state.data)
               }
              else {
                this.deleteFile(this.state.data)
                this.setState({date : null, pictureTaken : false})
              }
             }}
          />
        </Dialog.Actions> */}
        <View
          style={{
            flex: 1,
            backgroundColor: 'transparent',
            flexDirection: 'row',
            justifyContent : 'space-around',
            height: 30
          }}>
          <Button raised secondary
            text="Discard"
            onPress = {() => {
              this.deleteFile(this.state.data)
              this.setState({date : null, pictureTaken : false})
            }}
            style = {{padding : 10}}
          />
          <Button raised primary
            text="Keep"
            onPress = {() => {
              this.savePicture(this.state.data);
              this.setState({date : null, pictureTaken : false});
            }}
          />
        </View>

      </Dialog>
    )
  }

  render() {
    return (
      <View style={styles.container}>
        {/* {this.state.showGallery ? this.renderGallery() : this.renderCamera()} */}
        {this.state.pictureTaken ? this.renderDialog() : (this.state.showGallery ? this.renderGallery() : this.renderCamera())}
      </View>
    );
  }
}

export default class Main extends Component {
    render() {
        return (
            <ThemeProvider uiTheme={uiTheme}>
              <App/>
            </ThemeProvider>
        );
    }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'ivory',
  },
  navigation: {
    flex: 1,
  },
  gallery: {
    flex: 1,
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  topRow : {
    marginTop : 25
  },
  flipButton: {
    flex: 0.3,
    height: 40,
    marginHorizontal: 2,
    marginBottom: 10,
    borderRadius: 8,
    borderColor: 'white',
    borderWidth: 1,
    padding: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  flipText: {
    color: 'white',
    fontSize: 15,
  },
  item: {
    margin: 4,
    backgroundColor: 'indianred',
    height: 35,
    width: 80,
    borderRadius: 5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  picButton: {
    backgroundColor: 'darkseagreen',
  },
  galleryButton: {
    backgroundColor: 'indianred',
  },
  row: {
    flexDirection: 'row',
  },
  picture: {
    width: 250,
    height: 250,
    margin: 0,
    resizeMode: 'contain',
  },
});
