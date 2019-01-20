function varargout = vowel_conversion(varargin)
% VOWEL_CONVERSION MATLAB code for vowel_conversion.fig
%      VOWEL_CONVERSION, by itself, creates a new VOWEL_CONVERSION or raises the existing
%      singleton*.
%
%      H = VOWEL_CONVERSION returns the handle to a new VOWEL_CONVERSION or the handle to
%      the existing singleton*.
%
%      VOWEL_CONVERSION('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in VOWEL_CONVERSION.M with the given input arguments.
%
%      VOWEL_CONVERSION('Property','Value',...) creates a new VOWEL_CONVERSION or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before vowel_conversion_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to vowel_conversion_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help vowel_conversion

% Last Modified by GUIDE v2.5 04-Oct-2017 19:35:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @vowel_conversion_OpeningFcn, ...
                   'gui_OutputFcn',  @vowel_conversion_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before vowel_conversion is made visible.
function vowel_conversion_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to vowel_conversion (see VARARGIN)

% Choose default command line output for vowel_conversion
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes vowel_conversion wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = vowel_conversion_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;

%1. OPEN AUDIO FILE 1 
% --- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    [filename,pathname]=uigetfile({'*.*';'*.wav'},'????');
    if isequal(filename,0)||isequal(pathname,0)
      errordlg('Choose nothing','Error');%
      return;
    else
    audio_original=[pathname,filename];
    set(handles.text3,'String',[filename]);
    [x, fs] = audioread(filename);
    disp(filename);
    disp(fs);
    handles.playeraudio1 = audioplayer(x,fs);
    [raw] = cam_formants(x, fs, filename);
    handles.formant_audio1= raw;
    handles.x= x;
    handles.fs=fs;
    guidata(hObject, handles);
    end

%2. OPEN AUDIO FILE 2
% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
    [filename2,pathname2]=uigetfile({'*.*';'*.wav'},'????');
    if isequal(filename2,0)||isequal(pathname2,0)
      errordlg('Choose nothing','Error');%
      return;
    else
    audio_original=[pathname2,filename2];
    set(handles.text4,'String',[filename2]);
    [x2, fs2] = audioread(filename2);
    handles.playeraudio2 = audioplayer(x2,fs2);
    disp(filename2);
    disp(fs2);
    [raw] = cam_formants(x2, fs2, filename2);
    handles.formant_audio2= raw;
    handles.fs=fs2;%Use fs for audio 2
    guidata(hObject, handles);
    end 

%ANALYSIS &SYNTHESIS
% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%formant-audio2 is the sound we atre changing to
disp(handles)
raw=handles.formant_audio1;

%All this computation is for audio 1.
x=handles.x;
fs=handles.fs;
f0_parameter = Harvest(x, fs);
spectrum_parameter = CheapTrick(x, fs, f0_parameter);
fft_size=spectrum_parameter.fft_size;
disp(fft_size)
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;
disp(frequency_axis')
source_parameter = D4C(x, fs, f0_parameter);

[diff_form1, diff_form2]=formant_difference(handles.formant_audio1(:,2:3), handles.formant_audio2(:,2:3));
[shiftconst_array1, shiftconst_array2] = formantshiftconst(diff_form1, diff_form2, handles.fs);
disp([shiftconst_array1, shiftconst_array2])
new_spectrogram= shiftwholewaveform_frame(spectrum_parameter.spectrogram,raw, abs(shiftconst_array1), shiftconst_array2,frequency_axis);
spectrum_parameter.spectrogram=new_spectrogram;
disp(length(spectrum_parameter.spectrogram))
y = Synthesis(source_parameter, spectrum_parameter);
disp('done');
handles.playeroutput = audioplayer(y,fs);
handles.y=y;
handles.new_spectrogram=new_spectrogram;
handles.output = hObject;  
guidata(hObject, handles);

% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
play(handles.playeraudio1);



% --- Executes on button press in pushbutton3.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
play(handles.playeroutput);



% --- Executes on button press in pushbutton7.
function pushbutton7_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton7 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
play(handles.playeraudio2);



function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
