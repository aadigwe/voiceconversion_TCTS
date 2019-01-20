function varargout = world_fomant_version1(varargin)
% WORLD_FOMANT_VERSION1 MATLAB code for world_fomant_version1.fig
%      WORLD_FOMANT_VERSION1, by itself, creates a new WORLD_FOMANT_VERSION1 or raises the existing
%      singleton*.
%
%      H = WORLD_FOMANT_VERSION1 returns the handle to a new WORLD_FOMANT_VERSION1 or the handle to
%      the existing singleton*.
%
%      WORLD_FOMANT_VERSION1('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in WORLD_FOMANT_VERSION1.M with the given input arguments.
%
%      WORLD_FOMANT_VERSION1('Property','Value',...) creates a new WORLD_FOMANT_VERSION1 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before world_fomant_version1_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to world_fomant_version1_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help world_fomant_version1

% Last Modified by GUIDE v2.5 29-Sep-2017 11:31:15

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @world_fomant_version1_OpeningFcn, ...
                   'gui_OutputFcn',  @world_fomant_version1_OutputFcn, ...
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


% --- Executes just before world_fomant_version1 is made visible.
function world_fomant_version1_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to world_fomant_version1 (see VARARGIN)

% Choose default command line output for world_fomant_version1
handles.output = hObject;
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs=global_data.fs;
% Update handles structure
guidata(hObject, handles);


% UIWAIT makes world_fomant_version1 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = world_fomant_version1_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


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


function edit2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2 as text
%        str2double(get(hObject,'String')) returns contents of edit2 as a double


% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3 as text
%        str2double(get(hObject,'String')) returns contents of edit3 as a double


% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

%AXES 1 PLOT
% --- Executes on button press in pushbutton6.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global_data= getappdata(0,'WAV_DATA');
x=global_data.wav;
fs=  global_data.fs;
filename = global_data.filename;
f0_parameter=global_data.f0_parameter;
time_pos= str2double(get(handles.edit3,'string'));
global_data.timepos=time_pos;
spectrum_parameter=Cheap_Trick_Gui(x, fs, f0_parameter,time_pos);
set(handles.text5,'String',['Frame length(ms):  ',num2str(length(spectrum_parameter.waveform)*1000/fs)]);
fft_size=spectrum_parameter.fft_size;
frequency_axis = (0 : fft_size - 1)' / fft_size * fs;

%%%%plots DATA

axes(handles.axes1);
hold off;
plot([0;frequency_axis(1:length(frequency_axis)/2)],spectrum_parameter.spectral_envelope)
%plot([0;frequency_axis(1:length(frequency_axis)/2)],20*log10(spectrum_parameter.spectral_envelope))
hold on;
[raw] = cam_formants(x, fs, filename);
time_array=raw(:,1);
for i=1:length(time_array)
    if  time_pos  == time_array(i)
        vline(raw(i,2:end),'r:')
        formants_freq=raw(i,2:end);
    end
end
%disp('original formants and position')    
%disp(formants_freq)
%%%%%%%APRROXIMATING VALUES OF  FROMANTS TO FREQUENCY AXIS%%%%%%5
%formants_freq

round_formants =[];
round_formants_pos=[];
for j=formants_freq
    [M,I] = min(abs(frequency_axis-j));
    round_formants=[round_formants frequency_axis(I)];
    round_formants_pos=[round_formants_pos I];
end 


title('Spectral Envelope')
xlabel('frequency (Hz)');
ylabel('amplitude (dB)');
%handles.formants_amp =formants_amp;
handles.time_pos=time_pos;
handles.formants_raw=raw;
handles.formants_freq =round_formants;
handles.formants_pos =round_formants_pos;
handles.frequency_axis=frequency_axis;
handles.spec_env =spectrum_parameter.spectral_envelope;
handles.output = hObject;
guidata(hObject, handles);

%SHIFT BUTTON
%--- Executes on button press in pushbutton5.
function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles = guidata(hObject);
spec_env=handles.spec_env;
raw=handles.formants_raw;
time_pos=handles.time_pos;
%formants_amp=handles.formants_amp;
formants_freq=handles.formants_freq;
formants_pos=handles.formants_pos;
frequency_axis=handles.frequency_axis;
frequency_axis=[0;frequency_axis(1:length(frequency_axis)/2)];

shift1_const= str2double(get(handles.edit1,'string'));
shift2_const= str2double(get(handles.edit2,'string'));

%1.
%[peakarray]=localise_valley(spec_env,formants_freq(2), formants_pos(2));
disp('aaaaaaaaaaaaaa')
[peakarray]=localise_valley(spec_env, formants_pos(1), spec_env(formants_pos(1)))
disp('aaaaaaaaaaaaaa')
[peakarray2]=localise_valley(spec_env, formants_pos(2), spec_env(formants_pos(2)))
disp('aaaaaaaaaaaaaa')
if shift1_const > (shift2_const + (formants_pos(2)-formants_pos(1))-(peakarray2(2,end)-peakarray2(2,1)))
      errordlg('Shift value exceeds threshold','Error');
else
[shifted_array]= shiftpeaks2(spec_env, peakarray,shift1_const,peakarray2,shift2_const);
[newarray]= fill_remove(spec_env,shifted_array,peakarray(2,:),peakarray2(2,:),shift1_const,shift2_const);
axes(handles.axes2);
hold off;
plot(frequency_axis,newarray)
hold on
time_array=raw(:,1);
for i=1:length(time_array)
    if  time_pos  == time_array(i)
        vline(raw(i,2:end),'r:')
        formants_freq=raw(i,2:end);
    end
end
handles.newarray=newarray;
end 
handles.freq_axis=frequency_axis;
handles.output = hObject;
guidata(hObject, handles);

%ORIGINAL VALUES PLOTTED
% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
spec_env=handles.spec_env;
freq_axis=handles.freq_axis;
f = figure;
t = uitable(f,'Data',[freq_axis, spec_env]);
%t = uitable(f,'Data',randi(100,10,3),'Position',[20 20 262 204]);

%SHIFTED VALUES
% --- Executes on button press in pushbutton4.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
newarray=handles.newarray;
freq_axis=handles.freq_axis;
f = figure;
disp(size(newarray))
t = uitable(f,'Data',[freq_axis, newarray']);


   



function edit4_Callback(hObject, eventdata, handles)
% hObject    handle to edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit4 as text
%        str2double(get(hObject,'String')) returns contents of edit4 as a double


% --- Executes during object creation, after setting all properties.
function edit4_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
