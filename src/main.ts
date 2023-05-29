import {initBooks} from './books';
import {initContributors} from './contributors';
import {initWallet} from './wallet';
import {initQuill} from './initQuill';
import {initQuillValueToInput} from './quillValueToInput';
import {initComments} from './comment';
import {initVote} from './vote';
import {initTheme} from './theme';
import {initApprove} from './approve';
import {initStar} from './star';
import {initMultipleInput} from './multipleInput';
import {rightClick} from './rightClick';
import {addSubCollection} from './addSubCollection';
import {addSection} from './addSection';
import {deleteSection} from './deleteSection';
import {renameSection} from './renameSection';
import {deleteCollection} from './deleteCollection';
import {deleteSubCollection} from './deleteSubCollection';
import {renameCollection} from './renameCollection';
import {renameSubCollection} from './renameSubCollection';
import {initQuillReadOnly} from './initQuillReadOnly';
import {initGoBack} from './tabGoBackBtn';
import {scroll} from './scroll';
import {copyLink} from './copyLink';
import {quickSearch} from './quickSearch';
import {flash} from './flash';
import {slashSearch} from './slashSearch';
import {initInterpretations} from './interpretations';

initQuillReadOnly();
initBooks();
initContributors();
initQuill();
initQuillValueToInput();
initWallet();
initComments();
initVote();
initTheme();
initApprove();
initStar();
initMultipleInput();
rightClick();
addSubCollection();
addSection();
deleteSection();
renameSection();
deleteCollection();
renameCollection();
deleteSubCollection();
renameSubCollection();
initGoBack();
scroll();
copyLink();
quickSearch();
flash();
slashSearch();
initInterpretations();
