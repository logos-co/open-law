import {initEditVersion} from './editVersion';
import {initDeleteVersion} from './deleteVersion';

export const initVersions = () => {
  initEditVersion();
  initDeleteVersion();
};
