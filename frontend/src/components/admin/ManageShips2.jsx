import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Input, Checkbox, Select, Steps } from 'antd';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { API_URL } from './api';
import EditableTable from './EditableTable';
import { getEntity } from './api';


const { Step } = Steps;

const ManageShips = () => {
  const [ships, setShips] = useState([]); // Ship data for the grid
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0); // Tracks multi-step progress
  const [formData, setFormData] = useState({
    shipname: '',
    description: '',
    capacity: '',
    restaurants: [],
    activities: [],
    rooms: [],
  });
  const [activities, setActivities] = useState([]);
  const [diningOptions, setDiningOptions] = useState([]);
  const [rooms, setRooms] = useState([]);

//   useEffect(() => {
//     // Replace with your API call to fetch initial grid data
//     fetch('/api/ships')
//       .then((res) => res.json())
//       .then((data) => setShips(data))
//       .catch((error) => console.error(error));
//   }, []);

  const openModal = async () => {
    setIsModalOpen(true);
    setCurrentStep(0);

    // Fetch Activities, Dining, and Rooms
    try {
      const [activitiesRes, diningRes, roomsRes] = await Promise.all([
        getEntity('activities'),
        getEntity('restaurants'),
        getEntity('room-types'),
      ]);
      setActivities(activitiesRes);
      setDiningOptions(diningRes);
      setRooms(roomsRes);
    } catch (error) {
      console.error('Error fetching options:', error);
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setFormData({
      name: '',
      description: '',
      capacity: '',
      activities: [],
      dining: [],
      rooms: [],
    });
  };

  const handleNext = () => {
    if (currentStep < 2) setCurrentStep(currentStep + 1);
  };

  const handlePrev = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(`${API_URL}/admin/ships/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const createdShip = await response.json();
        setShips([...ships, createdShip]);
        closeModal();
        alert('Ship added successfully!');
      } else {
        throw new Error('Failed to add ship');
      }
    } catch (error) {
      console.error('Error adding ship:', error);
      alert('Error adding ship!');
    }
  };

  const handleFormChange = (key, value) => {
    setFormData((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div>
      <Button onClick={openModal} type="primary" style={{ marginBottom: '20px' }}>
        Add Ship
      </Button>

      {/* <div className="ag-theme-alpine" style={{ height: 400, width: '100%' }}>
        <AgGridReact
          rowData={ships}
          columnDefs={[
            { headerName: 'Name', field: 'name', sortable: true, filter: true },
            { headerName: 'Description', field: 'description', sortable: true, filter: true },
            { headerName: 'Capacity', field: 'capacity', sortable: true, filter: true },
          ]}
        />
      </div> */}

      <EditableTable entity="ships" data={data}/>

      <Modal
        title="Add Ship"
        open={isModalOpen}
        onCancel={closeModal}
        footer={null}
      >
        <Steps current={currentStep} style={{ marginBottom: '20px' }}>
          <Step title="Basic Details" />
          <Step title="Activities & Dining" />
          <Step title="Rooms" />
        </Steps>

        {currentStep === 0 && (
          <Form layout="vertical">
            <Form.Item label="Ship Name" required>
              <Input
                value={formData.shipname}
                onChange={(e) => handleFormChange('shipname', e.target.value)}
              />
            </Form.Item>
            <Form.Item label="Description">
              <Input.TextArea
                value={formData.description}
                onChange={(e) => handleFormChange('description', e.target.value)}
              />
            </Form.Item>
            <Form.Item label="Capacity" required>
              <Input
                type="number"
                value={formData.capacity}
                onChange={(e) => handleFormChange('capacity', e.target.value)}
              />
            </Form.Item>
          </Form>
        )}

        {currentStep === 1 && (
          <>
            <h4>Select Activities</h4>
            {activities.map((activity, idx) => (
              <Checkbox
                key={`${activity.activityid}-${idx}`}
                checked={formData.activities.includes(activity.activityid)}
                onChange={(e) => {
                  if (e.target.checked)
                    handleFormChange('activities', [...formData.activities, activity.activityid]);
                  else
                    handleFormChange(
                      'activities',
                      formData.activities.filter((id) => id !== activity.activityid)
                    );
                }}
              >
                {activity.activityname}
              </Checkbox>
            ))}
            <h4>Select Dining Options</h4>
            {diningOptions.map((dining) => (
              <Checkbox
                key={dining.id}
                checked={formData.dining.includes(dining.id)}
                onChange={(e) => {
                  if (e.target.checked)
                    handleFormChange('dining', [...formData.dining, dining.id]);
                  else
                    handleFormChange(
                      'dining',
                      formData.dining.filter((id) => id !== dining.id)
                    );
                }}
              >
                {dining.name}
              </Checkbox>
            ))}
          </>
        )}

        {currentStep === 2 && (
          <>
            <h4>Select Rooms</h4>
            {rooms.map((room) => (
              <Checkbox
                key={room.id}
                checked={formData.rooms.includes(room.id)}
                onChange={(e) => {
                  if (e.target.checked)
                    handleFormChange('rooms', [...formData.rooms, room.id]);
                  else
                    handleFormChange(
                      'rooms',
                      formData.rooms.filter((id) => id !== room.id)
                    );
                }}
              >
                {room.number}
              </Checkbox>
            ))}
          </>
        )}

        <div style={{ marginTop: '20px', textAlign: 'right' }}>
          {currentStep > 0 && <Button onClick={handlePrev} style={{ marginRight: '8px' }}>Previous</Button>}
          {currentStep < 2 && <Button onClick={handleNext}>Next</Button>}
          {currentStep === 2 && (
            <Button onClick={handleSubmit} type="primary">
              Submit
            </Button>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default ManageShips;
