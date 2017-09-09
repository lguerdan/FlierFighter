import React from 'react';
import {
  Image,
  StyleSheet,
  View,
  TouchableOpacity,
  Text,
  ScrollView,
  TouchableHighlight
} from 'react-native';
import { FileSystem } from 'expo';
import { Button } from 'react-native-material-ui';

export default class GalleryScreen extends React.Component {
  state = {
    enableDelete: false,
    fileToDelete : null
  };

  componentDidMount() {
    FileSystem.readDirectoryAsync(
      FileSystem.documentDirectory + 'photos'
    ).then(photos => this.props.updatePhotos(photos));
  }



  renderDeleteButton = () => {
    if (this.props.deletePhotoInfo.enabled){
      return(<Button raised secondary
        text="Delete"
        onPress = {() => console.log('delete',this.props.deleteFile(this.props.deletePhotoInfo.fileName))}/>)
    }else{
      return <View />
    }
  }


  render() {
    console.log(this.props)
    return (
      <View style={styles.container}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={this.props.onPress}>
          <Text>Back</Text>
        </TouchableOpacity>
        <ScrollView contentComponentStyle={{ flex: 1 }}>
          <View style={styles.pictures}>
            {this.props.photos.map(photoUri =>
              <TouchableHighlight
                key = {photoUri}
                onLongPress = { () => {this.props.onLongPress(photoUri)}}
                onPress = { () => {this.props.onLongPress(null)}}
                >
                <Image
                  style={styles.picture}
                  source={{
                    uri: `${FileSystem.documentDirectory}photos/${photoUri}`,
                  }}
                  key={photoUri}
                />
              </TouchableHighlight>

            )}
          </View>
        </ScrollView>
        {this.renderDeleteButton()}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
  },
  pictures: {
    flex: 1,
    flexWrap: 'wrap',
    flexDirection: 'row',
  },
  picture: {
    width: 100,
    height: 100,
    margin: 5,
    resizeMode: 'contain',
  },
  backButton: {
    padding: 20,
    marginBottom: 4,
    backgroundColor: 'indianred',
  },
});
