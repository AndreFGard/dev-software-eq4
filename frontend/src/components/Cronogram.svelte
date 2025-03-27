<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog";
    import * as Alert from "$lib/components/ui/alert";
    import {createSchedule} from "../api.js";
    import '../app.css';
    import type {Schedule} from "../api.ts";
    import { username } from "../api";
    export let schedule: Schedule | null = {
        title: "Conference Schedule 2024",
        days: [
            {
                day: 1,
                activities: [
                    {
                        time: "09:00",
                        name: "Registration & Coffee",
                        duration: "1h",
                        end_time: "10:00",
                        description: "Check-in and welcome coffee",
                        explanations: "Badges will be provided at the registration desk"
                    },
                    {
                        time: "10:00",
                        name: "Keynote Speech",
                        duration: "2h",
                        end_time: "12:00",
                        description: "Opening keynote by Dr. Smith",
                        explanations: "Main Auditorium - Level 1"
                    }
                ]
            },
            {
                day: 2,
                activities: [
                    {
                        time: "09:30",
                        name: "Workshop A",
                        duration: "3h",
                        end_time: "12:30",
                        description: "Hands-on coding session",
                        explanations: "Bring your laptop"
                    },
                    {
                        time: "14:00",
                        name: "Panel Discussion",
                        duration: "1.5h",
                        end_time: "15:30",
                        description: "Future of Technology",
                        explanations: null
                    }
                ]
            }
        ],
        explanations: "All sessions include Q&A time. Lunch break is from 12:30 to 14:00 each day."
    };
</script>

<Dialog.Root>

    <Dialog.Trigger class="button">Open Schedule</Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[70vw] w-[100vw] px-4 shadow">
        <Dialog.Header>
            <Dialog.Title>{"Schedule"}</Dialog.Title>
        </Dialog.Header>
        <div id="schedule-content" class="max-h-[70vh] overflow-y-auto px-6 py-2">
            {#if schedule != null}
                <div >
                    {#each schedule.days as day}
                        <div class="mb-6">
                            <h3 class="title is-4 mb-3">Day {day.day}</h3>
                            <div class="table-container">
                                <table class="table is-striped is-hoverable is-fullwidth">
                                    <thead>
                                        <tr>
                                            <th>Time</th>
                                            <th>Activity</th>
                                            <th>Duration</th>
                                            <th class="is-hidden-mobile">End</th>
                                            <th>Description</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each day.activities as activity}
                                            <tr>
                                                <td>{activity.time}</td>
                                                <td>{activity.name}</td>
                                                <td>{activity.duration}</td>
                                                <td class="is-hidden-mobile">{activity.end_time}</td>
                                                <td>
                                                    {activity.description}
                                                    {#if activity.explanations}
                                                        <p class="help">{activity.explanations}</p>
                                                    {/if}
                                                </td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    {/each}
                </div>
                {#if schedule.explanations}
                    <div class="mt-6 px-4">
                        <h4 class="title is-5 mb-2">Additional Information</h4>
                        <p class="content">{schedule.explanations}</p>
                    </div>
                {/if}
        {:else}
            <div class="flex justify-center">
                <div class="w-full sm:w-auto">
                    <Alert.Root>
                        <Alert.Title>No schedule available</Alert.Title>
                        <Alert.Description>Please create a Schedule with the button below</Alert.Description>
                    </Alert.Root>
                </div>
            </div>
        {/if}
        </div>
    <Dialog.Footer class=''>
        <button onclick={async () => schedule = await createSchedule($username)} class='button is-primary has-text-black'>
            {schedule === null ? '':"Re"}create Schedule
        </button>
    </Dialog.Footer>    
    </Dialog.Content>
</Dialog.Root>
