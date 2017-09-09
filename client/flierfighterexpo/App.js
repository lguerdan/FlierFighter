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
import { COLOR, ThemeProvider,Button, Toolbar } from 'react-native-material-ui';

import GalleryScreen from './components/GalleryScreen';

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
    type: 'back',
    whiteBalance: 'auto',
    ratio: '16:9',
    ratios: [],
    photoId: 1,
    showGallery: false,
    photos: [],
  };

  componentDidMount() {
    FileSystem.makeDirectoryAsync(
      FileSystem.documentDirectory + 'photos'
    ).catch(e => {
      console.log(e, 'Directory exists');
      FileSystem.readDirectoryAsync(
        FileSystem.documentDirectory + 'photos'
      ).then(photos => {
        this.updatePhotos(photos)
        this.setState({photoId : photos.length + 1});
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

  takePicture = async function() {
    if (this.camera) {
      this.camera.takePictureAsync().then(data => {
        FileSystem.moveAsync({
          from: data,
          to: `${FileSystem.documentDirectory}photos/Photo_${this.state
            .photoId}.jpg`,
        }).then(() => {
          const photoId = this.state.photoId + 1;
          this.setState({
            photoId
          });
          Vibration.vibrate();
        });
      });
    }
  };

  renderGallery() {
    return <GalleryScreen
      onPress={this.toggleView.bind(this)}
      updatePhotos = {this.updatePhotos}
      photos = {this.state.photos}
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
          {/* <TouchableOpacity
            style={[
              styles.flipButton,
              styles.picButton,
              { flex: 0.3, alignSelf: 'flex-end' },
            ]}
            onPress={this.takePicture.bind(this)}>
            <Text style={styles.flipText}> SNAP </Text>
          </TouchableOpacity> */}
          {/* <TouchableOpacity
            style={[
              styles.flipButton,
              styles.galleryButton,
              { flex: 0.25, alignSelf: 'flex-end' },
            ]}
            onPress={this.toggleView.bind(this)}>
            <Text style={styles.flipText}> Gallery </Text>
          </TouchableOpacity> */}
        </View>
        <SubmitButton onPress = {this.takePicture.bind(this)} />
      </Camera>
    );
  }

  render() {
    return (
      <View style={styles.container}>
        {this.state.showGallery ? this.renderGallery() : this.renderCamera()}
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
});
