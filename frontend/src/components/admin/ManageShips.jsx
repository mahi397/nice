import React, { useState, useEffect } from 'react';
import { Modal, Button, Form, Checkbox, Input, Select, Steps, message } from 'antd';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import { API_URL } from '../../constants';
import EditableTable from './EditableTable';
import { getEntity } from './api';

const ManageShips = ({ data }) => {
  const [ships, setShips] = useState(data); // Ship data for the grid
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentStep, setCurrentStep] = useState(0); // Track multi-step form progress
  const [shipName, setShipName] = useState(''); // Holds form data
  const [shipDescription, setShipDescription] = useState(''); // Holds form data
  const [shipCapacity, setShipCapacity] = useState(''); // Holds form data
  const [activities, setActivities] = useState([]);
  const [diningOptions, setDiningOptions] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [selectedActivities, setSelectedActivities] = useState([]);
  const [selectedDining, setSelectedDining] = useState([]);
  const [selectedRooms, setSelectedRooms] = useState([]);

  // Fetch initial data for AG-Grid
//   useEffect(() => {
//     let token = localStorage.getItem("authToken");
//     fetch(`${API_URL}/admin/ships/list`,{
//         headers: {
//           'Authorization': `Bearer ${token}`
//         }
//       })
//       .then((res) => res.json())
//       .then((data) => setShips(data))
//       .catch((error) => console.error(error));
//   }, []);

  const openModal = async () => {
    setIsModalOpen(true);
    setCurrentStep(0); // Reset stepper

    // Fetch Activities, Dining, and Rooms
    try {
      const [activitiesRes, diningRes, roomsRes] = await Promise.all([
        // fetch(`${API_URL}/admin/activities/list`).then((res) => res.json()),
        // fetch(`${API_URL}/admin/restaurants/list`).then((res) => res.json()),
        // fetch(`${API_URL}/admin/room-types/list`).then((res) => res.json()),
        getEntity('activities'),
        getEntity('restaurants'),
        getEntity('room-types'),
      ]);
    //   console.log("ACtivity: ", activitiesRes);
    //   console.log(diningRes);
    //   console.log(roomsRes);
      setActivities(activitiesRes);
      setDiningOptions(diningRes);
      setRooms(roomsRes);
    } catch (error) {
      console.error('Error fetching options:', error);
    }
  };

  const handleNext = () => {
    if (currentStep < 2) setCurrentStep(currentStep + 1);
  };

  const handlePrev = () => {
    if (currentStep > 0) setCurrentStep(currentStep - 1);
  };

  const handleSubmit = async () => {
    const newShip = {
      shipname: shipName,
      description: shipDescription,
      capacity: shipCapacity,
      restaurants: selectedDining,
      activities: selectedActivities,
      rooms: selectedRooms,
    };

    try {
      const response = await fetch(`${API_URL}/admin/ships/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newShip),
      });
      if (response.ok) {
        const createdShip = await response.json();
        setShips([...ships, createdShip]); // Update grid
        message.success('Ship added successfully!');
        setIsModalOpen(false); // Close modal
      } else {
        throw new Error('Failed to add ship');
      }
    } catch (error) {
      message.error('Error adding ship!');
      console.error(error);
    }
  };

  const steps = [
    {
      title: 'Basic Details',
      content: (
        <Form layout="vertical" initialValues={{ selectedActivities, selectedDining }}>
          <Form.Item label="Ship Name" required>
            <Input onChange={(e) => setShipName({ shipName, name: e.target.value })} />
          </Form.Item>
          <Form.Item label="Description">
            <Input.TextArea onChange={(e) => setShipDescription({ shipDescription, description: e.target.value })} />
          </Form.Item>
          <Form.Item label="Capacity" required>
            <Input
              type="number"
              onChange={(e) => setShipCapacity({ shipCapacity, capacity: e.target.value })}
            />
          </Form.Item>
        </Form>
      ),
    },
    {
      title: 'Activities & Dining',
      content: (
        <>
          <h4>Select Activities:</h4>
          {activities.map((activity, idx) => (
            <Checkbox
              key={`${activity.activityid}-${idx}`}
              checked={selectedActivities.includes(activity.activityid)}
              onChange={(e) => {
                if (e.target.checked) setSelectedActivities([...selectedActivities, activity.activityid]);
                else setSelectedActivities(selectedActivities.filter((id) => id !== activity.activityid));
              }}
            >
              {activity.activityname}
            </Checkbox>
          ))}
          <h4 style={{ marginTop: '20px' }}>Select Dining Options:</h4>
          {diningOptions.map((restaurant, idx) => (
            <Checkbox
              key={`${restaurant.restaurantid}-${idx}`}
              checked={selectedDining.includes(restaurant.restaurantid)}
              onChange={(e) => {
                if (e.target.checked) setSelectedDining([...selectedDining, restaurant.restaurantid]);
                else setSelectedDining(selectedDining.filter((id) => id !== restaurant.restaurantid));
              }}
            >
              {restaurant.restaurantname}
            </Checkbox>
          ))}
        </>
      ),
    },
    {
      title: 'Rooms',
      content: (
        <>
          <h4>Select Rooms:</h4>
          {rooms.map((room, idx) => (
            <Checkbox
              key={`${room.stateroomtypeid}-${idx}`}
              onChange={(e) => {
                if (e.target.checked) setSelectedRooms([...selectedRooms, room.stateroomtypeid]);
                else setSelectedRooms(selectedRooms.filter((id) => id !== room.stateroomtypeid));
              }}
            >
              {room.stateroomtypeid}
            </Checkbox>
          ))}
        </>
      ),
    },
  ];

  return (
    <div>
      <Button type="primary" onClick={openModal}>
        Add Ship
      </Button>
      {/* <div className="ag-theme-alpine" style={{ height: 400, width: '100%', marginTop: 20 }}>
        <AgGridReact
          rowData={ships}
          columnDefs={[
            { headerName: 'Name', field: 'name', sortable: true, filter: true },
            { headerName: 'Description', field: 'description', sortable: true, filter: true },
            { headerName: 'Capacity', field: 'capacity', sortable: true, filter: true },
            // { headerName: 'Restaurants', field: 'capacity', sortable: false, filter: true },
            // { headerName: 'Activities', field: 'capacity', sortable: false, filter: true },
            // { headerName: 'Rooms', field: 'capacity', sortable: false, filter: true },
            
          ]}
        />
      </div> */}
      <EditableTable entity="ships" data={data}/>
      
      <Modal
        title="Add Ship"
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        width={800}
      >
        <Steps current={currentStep}>
          {steps.map((item) => (
            <Steps.Step key={item.title} title={item.title} />
          ))}
        </Steps>
        <div style={{ marginTop: 20 }}>{steps[currentStep].content}</div>
        <div style={{ marginTop: 20, display: 'flex', justifyContent: 'space-between'}}>
          {currentStep > 0 && <Button onClick={handlePrev}>Previous</Button>}
          {currentStep < steps.length - 1 && <Button onClick={handleNext}>Next</Button>}
          {currentStep === steps.length - 1 && (
            <Button type="primary" onClick={handleSubmit}>
              Submit
            </Button>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default ManageShips;
