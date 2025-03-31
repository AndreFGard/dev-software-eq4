<script lang="ts">
    import * as Dialog from "$lib/components/ui/dialog";
    import * as Alert from "$lib/components/ui/alert";
    import {createSchedule, getSchedule} from "../api.js";
    import '../app.css';
    import type {Schedule} from "../api.ts";
    import { username } from "../api";
    export let schedule: Schedule | null = null;
    import LoaderCircle from "lucide-svelte/icons/loader-circle";

    let loadingSchedule = false;

    async function getScheduleView(){
        loadingSchedule = true;
        schedule = await getSchedule($username);
        loadingSchedule = false;
    }
    async function createScheduleView(){
        loadingSchedule = true;
        schedule = await createSchedule($username);
        loadingSchedule = false;
    }

    getScheduleView().then(() => {
        console.log("Schedule loaded");
    }).catch((error) => {
        console.error("Error loading schedule:", error);
    });


</script>

<Dialog.Root>

    <Dialog.Trigger class="button">Open Schedule</Dialog.Trigger>
    <Dialog.Content class="sm:max-w-[70vw] w-[100vw] px-4  rounded-xl">
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
        <button onclick={async () => {await createScheduleView()}} class='button is-primary has-text-black {loadingSchedule ? 'grayscale' : ''}'>
            {#if loadingSchedule}
                <LoaderCircle class="animate-spin h-4 w-4 mr-2" />
                Loading
            {:else}
                {schedule === null ? 'Re':""}fresh
            {/if}            
        </button>
        <button onclick={async () => await getScheduleView()} class="button is-light {loadingSchedule ? 'grayscale' : ''}">
            {#if loadingSchedule}
                <LoaderCircle class="animate-spin h-4 w-4 mr-2" />
                Loading
            {:else}
                Refresh
            {/if}
        </button>
    </Dialog.Footer>    
    </Dialog.Content>
</Dialog.Root>
